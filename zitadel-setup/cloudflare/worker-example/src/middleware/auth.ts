/**
 * ZITADEL JWT Validation Middleware for Cloudflare Workers
 *
 * Features:
 * - JWKS caching for performance
 * - Role extraction from ZITADEL claims
 * - Multi-tenant context from JWT
 * - Proper error handling
 */

import { createRemoteJWKSet, jwtVerify, JWTPayload } from 'jose'
import { Context, Next } from 'hono'

// ZITADEL-specific JWT claims
export interface ZitadelClaims extends JWTPayload {
  // Standard claims
  sub: string
  email?: string
  name?: string
  preferred_username?: string

  // ZITADEL-specific claims
  'urn:zitadel:iam:org:id'?: string
  'urn:zitadel:iam:org:name'?: string
  'urn:zitadel:iam:org:domain:primary'?: string
  'urn:zitadel:iam:org:project:roles'?: Record<string, Record<string, string>>
  'urn:zitadel:iam:user:resourceowner'?: string
}

export interface AuthContext {
  userId: string
  email: string | null
  name: string | null
  organizationId: string | null
  organizationName: string | null
  roles: string[]
  claims: ZitadelClaims
  // Role helpers
  isSuperAdmin: boolean
  isOrgAdmin: boolean
  isEditor: boolean
  isViewer: boolean
}

// Environment variables expected by the worker
export interface Env {
  ZITADEL_ISSUER: string
  ZITADEL_AUDIENCE?: string
  // Optional: KV namespace for JWKS caching
  JWKS_CACHE?: KVNamespace
}

// JWKS cache (in-memory, refreshed on cold starts)
let jwksCache: ReturnType<typeof createRemoteJWKSet> | null = null

function getJWKS(issuer: string): ReturnType<typeof createRemoteJWKSet> {
  if (!jwksCache) {
    const jwksUri = new URL('/.well-known/jwks.json', issuer)
    jwksCache = createRemoteJWKSet(jwksUri)
  }
  return jwksCache
}

/**
 * Extract Bearer token from Authorization header
 */
function extractBearerToken(authHeader: string | undefined): string | null {
  if (!authHeader) return null
  const [type, token] = authHeader.split(' ')
  if (type?.toLowerCase() !== 'bearer' || !token) return null
  return token
}

/**
 * Parse ZITADEL roles from claims
 * Roles are stored as: { "role_name": { "org_id": "org_name" } }
 */
function parseRoles(rolesClaim: ZitadelClaims['urn:zitadel:iam:org:project:roles']): string[] {
  if (!rolesClaim) return []
  return Object.keys(rolesClaim)
}

/**
 * Build AuthContext from validated JWT claims
 */
function buildAuthContext(claims: ZitadelClaims): AuthContext {
  const roles = parseRoles(claims['urn:zitadel:iam:org:project:roles'])

  return {
    userId: claims.sub,
    email: claims.email || null,
    name: claims.name || claims.preferred_username || null,
    organizationId: claims['urn:zitadel:iam:org:id'] || null,
    organizationName: claims['urn:zitadel:iam:org:name'] || null,
    roles,
    claims,
    // Role hierarchy helpers
    isSuperAdmin: roles.includes('super_admin'),
    isOrgAdmin: roles.includes('org_admin') || roles.includes('super_admin'),
    isEditor: roles.includes('editor') || roles.includes('org_admin') || roles.includes('super_admin'),
    isViewer: roles.includes('viewer') || roles.includes('editor') || roles.includes('org_admin') || roles.includes('super_admin'),
  }
}

/**
 * JWT Authentication Middleware
 */
export function authMiddleware() {
  return async (c: Context<{ Bindings: Env; Variables: { auth: AuthContext } }>, next: Next) => {
    const env = c.env

    // Validate configuration
    if (!env.ZITADEL_ISSUER) {
      console.error('ZITADEL_ISSUER not configured')
      return c.json({ error: 'Server configuration error' }, 500)
    }

    // Extract token
    const authHeader = c.req.header('Authorization')
    const token = extractBearerToken(authHeader)

    if (!token) {
      return c.json({ error: 'Missing or invalid Authorization header' }, 401)
    }

    try {
      // Validate JWT
      const jwks = getJWKS(env.ZITADEL_ISSUER)

      const { payload } = await jwtVerify(token, jwks, {
        issuer: env.ZITADEL_ISSUER,
        audience: env.ZITADEL_AUDIENCE || undefined,
      })

      // Build auth context
      const authContext = buildAuthContext(payload as ZitadelClaims)

      // Attach to request context
      c.set('auth', authContext)

      await next()
    } catch (error) {
      console.error('JWT validation failed:', error)

      if (error instanceof Error) {
        if (error.message.includes('expired')) {
          return c.json({ error: 'Token expired' }, 401)
        }
        if (error.message.includes('signature')) {
          return c.json({ error: 'Invalid token signature' }, 401)
        }
      }

      return c.json({ error: 'Invalid token' }, 401)
    }
  }
}

/**
 * Role-based access control middleware
 * Requires authMiddleware to run first
 */
export function requireRole(role: 'super_admin' | 'org_admin' | 'editor' | 'viewer') {
  return async (c: Context<{ Variables: { auth: AuthContext } }>, next: Next) => {
    const auth = c.get('auth')

    if (!auth) {
      return c.json({ error: 'Not authenticated' }, 401)
    }

    const hasRole = {
      super_admin: auth.isSuperAdmin,
      org_admin: auth.isOrgAdmin,
      editor: auth.isEditor,
      viewer: auth.isViewer,
    }[role]

    if (!hasRole) {
      return c.json(
        {
          error: 'Forbidden',
          message: `Required role: ${role}`,
          userRoles: auth.roles,
        },
        403
      )
    }

    await next()
  }
}

/**
 * Tenant isolation middleware
 * Ensures users can only access resources in their organization
 * Super admins bypass this check
 */
export function requireTenant(getResourceOrgId: (c: Context) => string | null) {
  return async (c: Context<{ Variables: { auth: AuthContext } }>, next: Next) => {
    const auth = c.get('auth')

    if (!auth) {
      return c.json({ error: 'Not authenticated' }, 401)
    }

    // Super admins can access any tenant
    if (auth.isSuperAdmin) {
      await next()
      return
    }

    const resourceOrgId = getResourceOrgId(c)

    // If no org context, allow (resource is not tenant-scoped)
    if (!resourceOrgId) {
      await next()
      return
    }

    // Check tenant match
    if (auth.organizationId !== resourceOrgId) {
      return c.json(
        {
          error: 'Forbidden',
          message: 'You cannot access resources in another organization',
        },
        403
      )
    }

    await next()
  }
}

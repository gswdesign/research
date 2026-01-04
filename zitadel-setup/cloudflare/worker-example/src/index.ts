/**
 * ZITADEL-Protected API using Cloudflare Workers + Hono
 *
 * Example API demonstrating:
 * - JWT authentication with ZITADEL
 * - Role-based access control
 * - Multi-tenant isolation
 * - Resource ownership checks
 */

import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'
import { authMiddleware, requireRole, requireTenant, AuthContext, Env } from './middleware/auth'

// Type-safe app with bindings and variables
type AppEnv = {
  Bindings: Env
  Variables: { auth: AuthContext }
}

const app = new Hono<AppEnv>()

// ============================================
// Global Middleware
// ============================================

// CORS - configure for your domains
app.use('*', cors({
  origin: ['http://localhost:3000', 'https://your-app.pages.dev'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization'],
  exposeHeaders: ['X-Request-Id'],
  credentials: true,
}))

// Request logging
app.use('*', logger())

// ============================================
// Public Routes (no auth required)
// ============================================

app.get('/', (c) => {
  return c.json({
    name: 'ZITADEL-Protected API',
    version: '1.0.0',
    docs: '/docs',
  })
})

app.get('/health', (c) => {
  return c.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// ============================================
// Protected Routes
// ============================================

// Apply auth middleware to all /api routes
const api = new Hono<AppEnv>()
api.use('*', authMiddleware())

// GET /api/me - Get current user info (any authenticated user)
api.get('/me', (c) => {
  const auth = c.get('auth')

  return c.json({
    user: {
      id: auth.userId,
      email: auth.email,
      name: auth.name,
      organizationId: auth.organizationId,
      organizationName: auth.organizationName,
      roles: auth.roles,
    },
    permissions: {
      isSuperAdmin: auth.isSuperAdmin,
      isOrgAdmin: auth.isOrgAdmin,
      isEditor: auth.isEditor,
      isViewer: auth.isViewer,
    },
  })
})

// ============================================
// Viewer Routes (read-only access)
// ============================================

api.get('/resources', requireRole('viewer'), (c) => {
  const auth = c.get('auth')

  // Example: Fetch resources scoped to user's organization
  // In real app, query your database with auth.organizationId filter
  const resources = [
    { id: '1', name: 'Resource 1', orgId: auth.organizationId },
    { id: '2', name: 'Resource 2', orgId: auth.organizationId },
  ]

  return c.json({
    data: resources,
    meta: {
      organizationId: auth.organizationId,
      total: resources.length,
    },
  })
})

api.get('/resources/:id', requireRole('viewer'), (c) => {
  const { id } = c.req.param()
  const auth = c.get('auth')

  // Example resource with ownership
  const resource = {
    id,
    name: `Resource ${id}`,
    orgId: auth.organizationId,
    ownerId: auth.userId, // The creator
    createdAt: new Date().toISOString(),
  }

  return c.json({ data: resource })
})

// ============================================
// Editor Routes (create/edit access)
// ============================================

api.post('/resources', requireRole('editor'), async (c) => {
  const auth = c.get('auth')
  const body = await c.req.json()

  // Create resource with automatic org and owner assignment
  const newResource = {
    id: crypto.randomUUID(),
    ...body,
    orgId: auth.organizationId,
    ownerId: auth.userId,
    createdAt: new Date().toISOString(),
  }

  return c.json({ data: newResource }, 201)
})

api.put('/resources/:id', requireRole('editor'), async (c) => {
  const { id } = c.req.param()
  const auth = c.get('auth')
  const body = await c.req.json()

  // Example: Check resource ownership for non-admins
  // In real app, fetch the resource and check ownerId
  const existingResource = {
    id,
    ownerId: 'some-user-id', // From database
    orgId: auth.organizationId,
  }

  // Viewers can only edit their own resources
  if (!auth.isOrgAdmin && existingResource.ownerId !== auth.userId) {
    return c.json(
      { error: 'You can only edit resources you own' },
      403
    )
  }

  const updatedResource = {
    ...existingResource,
    ...body,
    updatedAt: new Date().toISOString(),
    updatedBy: auth.userId,
  }

  return c.json({ data: updatedResource })
})

// ============================================
// Admin Routes (organization management)
// ============================================

api.get('/admin/users', requireRole('org_admin'), (c) => {
  const auth = c.get('auth')

  // List users in the organization
  // In real app, query ZITADEL API or your user store
  return c.json({
    data: [
      { id: '1', email: 'user1@example.com', role: 'editor' },
      { id: '2', email: 'user2@example.com', role: 'viewer' },
    ],
    meta: {
      organizationId: auth.organizationId,
    },
  })
})

api.post('/admin/invite', requireRole('org_admin'), async (c) => {
  const auth = c.get('auth')
  const { email, role } = await c.req.json()

  // Validate role assignment
  // Org admins can only assign roles up to their level
  const allowedRoles = ['viewer', 'editor']
  if (auth.isSuperAdmin) {
    allowedRoles.push('org_admin')
  }

  if (!allowedRoles.includes(role)) {
    return c.json(
      { error: `Cannot assign role: ${role}` },
      403
    )
  }

  // In real app, call ZITADEL API to create user invite
  return c.json({
    message: 'Invitation sent',
    data: {
      email,
      role,
      organizationId: auth.organizationId,
      invitedBy: auth.userId,
    },
  })
})

// ============================================
// Super Admin Routes (cross-tenant access)
// ============================================

api.get('/super-admin/organizations', requireRole('super_admin'), (c) => {
  // List all organizations
  return c.json({
    data: [
      { id: 'org-1', name: 'Acme Corp', userCount: 50 },
      { id: 'org-2', name: 'Widget Inc', userCount: 25 },
    ],
  })
})

api.get('/super-admin/organizations/:orgId/resources', requireRole('super_admin'), (c) => {
  const { orgId } = c.req.param()

  // Super admin can access any organization's resources
  return c.json({
    data: [
      { id: '1', name: 'Resource 1', orgId },
      { id: '2', name: 'Resource 2', orgId },
    ],
    meta: { organizationId: orgId },
  })
})

// ============================================
// Mount API routes
// ============================================

app.route('/api', api)

// ============================================
// Error Handling
// ============================================

app.notFound((c) => {
  return c.json({ error: 'Not found' }, 404)
})

app.onError((err, c) => {
  console.error('Unhandled error:', err)
  return c.json(
    {
      error: 'Internal server error',
      message: err.message,
    },
    500
  )
})

export default app

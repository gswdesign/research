/**
 * ZITADEL Authentication for Cloudflare Pages SPA
 *
 * Uses PKCE flow (no client secret required for SPAs)
 * Tokens stored in memory for security (not localStorage)
 */

import { UserManager, WebStorageStateStore, User } from 'oidc-client-ts'

// Configuration - set these in your Cloudflare Pages environment variables
const ZITADEL_AUTHORITY = import.meta.env.VITE_ZITADEL_AUTHORITY
const CLIENT_ID = import.meta.env.VITE_ZITADEL_CLIENT_ID
const REDIRECT_URI = import.meta.env.VITE_REDIRECT_URI
const POST_LOGOUT_REDIRECT_URI = import.meta.env.VITE_POST_LOGOUT_REDIRECT_URI

// Singleton user manager
let userManager: UserManager | null = null

export function createUserManager(): UserManager {
  if (!userManager) {
    if (!ZITADEL_AUTHORITY || !CLIENT_ID) {
      throw new Error('ZITADEL configuration missing. Set VITE_ZITADEL_AUTHORITY and VITE_ZITADEL_CLIENT_ID')
    }

    userManager = new UserManager({
      authority: ZITADEL_AUTHORITY,
      client_id: CLIENT_ID,
      redirect_uri: REDIRECT_URI || `${window.location.origin}/callback`,
      post_logout_redirect_uri: POST_LOGOUT_REDIRECT_URI || window.location.origin,
      scope: 'openid profile email urn:zitadel:iam:org:project:id:zitadel:aud',
      response_type: 'code',
      // Use session storage for state only, tokens stay in memory
      userStore: new WebStorageStateStore({ store: window.sessionStorage }),
      automaticSilentRenew: true,
      // Silent renew in iframe
      silentRequestTimeoutInSeconds: 30,
    })

    // Handle token expiration
    userManager.events.addAccessTokenExpiring(() => {
      console.log('Token expiring, will refresh...')
    })

    userManager.events.addAccessTokenExpired(() => {
      console.log('Token expired')
    })

    userManager.events.addUserSignedOut(() => {
      console.log('User signed out')
      window.location.href = '/'
    })
  }

  return userManager
}

// Authentication Functions

export async function login(): Promise<void> {
  const manager = createUserManager()
  // Store current location to redirect back after login
  sessionStorage.setItem('returnUrl', window.location.pathname)
  await manager.signinRedirect()
}

export async function handleLoginCallback(): Promise<User> {
  const manager = createUserManager()
  const user = await manager.signinRedirectCallback()
  return user
}

export async function logout(): Promise<void> {
  const manager = createUserManager()
  await manager.signoutRedirect()
}

export async function getUser(): Promise<User | null> {
  const manager = createUserManager()
  return await manager.getUser()
}

export async function getAccessToken(): Promise<string | null> {
  const user = await getUser()
  if (!user || user.expired) {
    return null
  }
  return user.access_token
}

export async function isAuthenticated(): Promise<boolean> {
  const user = await getUser()
  return !!user && !user.expired
}

// Role and Permission Helpers

export interface UserInfo {
  id: string
  email: string
  name: string
  roles: string[]
  organizationId: string | null
  isSuperAdmin: boolean
  isOrgAdmin: boolean
  isEditor: boolean
  isViewer: boolean
}

export function parseUserInfo(user: User): UserInfo {
  const claims = user.profile

  // ZITADEL role claim structure
  const rolesObj = claims['urn:zitadel:iam:org:project:roles'] as Record<string, unknown> | undefined
  const roles = rolesObj ? Object.keys(rolesObj) : []

  const organizationId = (claims['urn:zitadel:iam:org:id'] as string) || null

  return {
    id: user.profile.sub,
    email: user.profile.email || '',
    name: user.profile.name || user.profile.preferred_username || '',
    roles,
    organizationId,
    isSuperAdmin: roles.includes('super_admin'),
    isOrgAdmin: roles.includes('org_admin') || roles.includes('super_admin'),
    isEditor: roles.includes('editor') || roles.includes('org_admin') || roles.includes('super_admin'),
    isViewer: roles.includes('viewer') || roles.includes('editor') || roles.includes('org_admin') || roles.includes('super_admin'),
  }
}

// API Call Helper with automatic token injection

export async function fetchWithAuth(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = await getAccessToken()

  if (!token) {
    throw new Error('Not authenticated')
  }

  const headers = new Headers(options.headers)
  headers.set('Authorization', `Bearer ${token}`)

  return fetch(url, {
    ...options,
    headers,
  })
}

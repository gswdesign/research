import { UserManager, WebStorageStateStore, User } from 'oidc-client-ts'

// Configuration from environment variables
const config = {
  authority: import.meta.env.VITE_ZITADEL_AUTHORITY || 'http://localhost:8080',
  client_id: import.meta.env.VITE_ZITADEL_CLIENT_ID || '',
  redirect_uri: import.meta.env.VITE_REDIRECT_URI || 'http://localhost:3000/callback',
  post_logout_redirect_uri: import.meta.env.VITE_POST_LOGOUT_REDIRECT_URI || 'http://localhost:3000',
  scope: 'openid profile email',
  response_type: 'code',
  // PKCE is required for SPAs (no client secret)
  // oidc-client-ts handles this automatically
}

// Create user manager for OIDC operations
let userManager: UserManager | null = null

export function getUserManager(): UserManager {
  if (!userManager) {
    userManager = new UserManager({
      authority: config.authority,
      client_id: config.client_id,
      redirect_uri: config.redirect_uri,
      post_logout_redirect_uri: config.post_logout_redirect_uri,
      scope: config.scope,
      response_type: config.response_type,
      userStore: new WebStorageStateStore({ store: window.sessionStorage }),
      // Automatic silent refresh
      automaticSilentRenew: true,
      // Include organization info in token
      extraQueryParams: {
        // Add any ZITADEL-specific params here
      },
    })
  }
  return userManager
}

// Initiate Google SSO login
export async function loginWithGoogle(): Promise<void> {
  const manager = getUserManager()
  // ZITADEL uses 'idp' query param to specify identity provider
  // The IDP ID for Google is configured in ZITADEL Console
  await manager.signinRedirect({
    extraQueryParams: {
      // Uncomment and set your Google IDP ID from ZITADEL
      // idp: 'your-google-idp-id',
    },
  })
}

// Initiate email/password login
// Note: For custom login UI, you'll use ZITADEL's Session API directly
export async function loginWithPassword(email: string, password: string): Promise<void> {
  // ZITADEL Session API endpoint
  const authority = config.authority

  // Create session using ZITADEL's Session API
  // This is a simplified example - production should handle all flows
  const response = await fetch(`${authority}/v2beta/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      checks: {
        user: {
          loginName: email,
        },
        password: {
          password: password,
        },
      },
    }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message || 'Login failed')
  }

  const session = await response.json()

  // After session creation, initiate OIDC flow
  // The session cookie will be used for authentication
  const manager = getUserManager()
  await manager.signinRedirect()
}

// Handle the callback after login redirect
export async function handleCallback(): Promise<User> {
  const manager = getUserManager()
  return await manager.signinRedirectCallback()
}

// Get current user
export async function getUser(): Promise<User | null> {
  const manager = getUserManager()
  return await manager.getUser()
}

// Logout
export async function logout(): Promise<void> {
  const manager = getUserManager()
  await manager.signoutRedirect()
}

// Check if user is authenticated
export async function isAuthenticated(): Promise<boolean> {
  const user = await getUser()
  return !!user && !user.expired
}

// Get access token
export async function getAccessToken(): Promise<string | null> {
  const user = await getUser()
  return user?.access_token || null
}

// Get user roles from token claims
export function getUserRoles(user: User): string[] {
  const claims = user.profile
  // ZITADEL stores roles in this claim
  const roles = claims['urn:zitadel:iam:org:project:roles'] as Record<string, unknown> | undefined
  return roles ? Object.keys(roles) : []
}

// Get organization ID from token
export function getOrganizationId(user: User): string | null {
  const claims = user.profile
  return (claims['urn:zitadel:iam:org:id'] as string) || null
}

// Check if user has specific role
export function hasRole(user: User, role: string): boolean {
  const roles = getUserRoles(user)
  return roles.includes(role)
}

// Check if user is super admin (cross-tenant access)
export function isSuperAdmin(user: User): boolean {
  return hasRole(user, 'super_admin')
}

// Check if user is org admin
export function isOrgAdmin(user: User): boolean {
  return hasRole(user, 'org_admin') || isSuperAdmin(user)
}

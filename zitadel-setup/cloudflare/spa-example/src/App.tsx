import React, { useEffect, useState, createContext, useContext, ReactNode } from 'react'
import {
  login,
  logout,
  handleLoginCallback,
  getUser,
  isAuthenticated,
  parseUserInfo,
  UserInfo,
  fetchWithAuth,
} from './auth'
import type { User } from 'oidc-client-ts'

// ============================================
// Auth Context
// ============================================

interface AuthContextType {
  user: UserInfo | null
  isLoading: boolean
  isAuthenticated: boolean
  login: () => Promise<void>
  logout: () => Promise<void>
  fetchWithAuth: typeof fetchWithAuth
}

const AuthContext = createContext<AuthContextType | null>(null)

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

// ============================================
// Auth Provider
// ============================================

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<UserInfo | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for existing session on mount
    const checkAuth = async () => {
      try {
        const oidcUser = await getUser()
        if (oidcUser && !oidcUser.expired) {
          setUser(parseUserInfo(oidcUser))
        }
      } catch (error) {
        console.error('Auth check failed:', error)
      } finally {
        setIsLoading(false)
      }
    }

    checkAuth()
  }, [])

  const handleLogin = async () => {
    await login()
  }

  const handleLogout = async () => {
    await logout()
    setUser(null)
  }

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login: handleLogin,
    logout: handleLogout,
    fetchWithAuth,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// ============================================
// Protected Route Component
// ============================================

interface ProtectedRouteProps {
  children: ReactNode
  requiredRole?: 'super_admin' | 'org_admin' | 'editor' | 'viewer'
}

export function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const { user, isLoading, isAuthenticated, login } = useAuth()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <h1 className="text-2xl font-bold">Please sign in</h1>
        <button
          onClick={login}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Sign In
        </button>
      </div>
    )
  }

  // Check role if required
  if (requiredRole && user) {
    const hasRole = {
      super_admin: user.isSuperAdmin,
      org_admin: user.isOrgAdmin,
      editor: user.isEditor,
      viewer: user.isViewer,
    }[requiredRole]

    if (!hasRole) {
      return (
        <div className="flex flex-col items-center justify-center min-h-screen gap-4">
          <h1 className="text-2xl font-bold text-red-600">Access Denied</h1>
          <p>You don't have permission to access this page.</p>
          <p className="text-sm text-gray-500">Required role: {requiredRole}</p>
        </div>
      )
    }
  }

  return <>{children}</>
}

// ============================================
// Callback Component
// ============================================

export function AuthCallback() {
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const processCallback = async () => {
      try {
        await handleLoginCallback()
        // Redirect to stored URL or dashboard
        const returnUrl = sessionStorage.getItem('returnUrl') || '/dashboard'
        sessionStorage.removeItem('returnUrl')
        window.location.href = returnUrl
      } catch (err) {
        console.error('Callback error:', err)
        setError(err instanceof Error ? err.message : 'Authentication failed')
      }
    }

    processCallback()
  }, [])

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <h1 className="text-2xl font-bold text-red-600">Authentication Failed</h1>
        <p className="text-gray-600">{error}</p>
        <a href="/" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
          Try Again
        </a>
      </div>
    )
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      <p className="text-gray-600">Completing sign in...</p>
    </div>
  )
}

// ============================================
// Example Dashboard Component
// ============================================

export function Dashboard() {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold">Dashboard</h1>
              <p className="text-gray-600">Welcome, {user?.name}</p>
            </div>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
            >
              Sign Out
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Your Profile</h2>
          <dl className="grid grid-cols-2 gap-4">
            <div>
              <dt className="text-sm text-gray-500">Email</dt>
              <dd className="font-medium">{user?.email}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">User ID</dt>
              <dd className="font-medium font-mono text-sm">{user?.id}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Organization</dt>
              <dd className="font-medium font-mono text-sm">{user?.organizationId || 'N/A'}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-500">Roles</dt>
              <dd className="flex gap-2 flex-wrap">
                {user?.roles.map((role) => (
                  <span
                    key={role}
                    className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded"
                  >
                    {role}
                  </span>
                ))}
              </dd>
            </div>
          </dl>
        </div>

        {/* Role-based content example */}
        {user?.isOrgAdmin && (
          <div className="bg-white rounded-lg shadow p-6 mt-6">
            <h2 className="text-lg font-semibold mb-4">Admin Panel</h2>
            <p className="text-gray-600">
              You have admin access. Manage your organization here.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

// ============================================
// Main App
// ============================================

export default function App() {
  // Simple routing based on pathname
  const path = window.location.pathname

  // Handle OAuth callback
  if (path === '/callback') {
    return <AuthCallback />
  }

  return (
    <AuthProvider>
      {path === '/dashboard' ? (
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      ) : (
        // Landing page
        <LandingPage />
      )}
    </AuthProvider>
  )
}

function LandingPage() {
  const { isAuthenticated, login, user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-xl p-8 max-w-md w-full text-center">
        <h1 className="text-3xl font-bold mb-2">Welcome</h1>
        <p className="text-gray-600 mb-8">
          Example SPA with ZITADEL authentication
        </p>

        {isAuthenticated ? (
          <div>
            <p className="mb-4">Signed in as {user?.name}</p>
            <a
              href="/dashboard"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Go to Dashboard
            </a>
          </div>
        ) : (
          <button
            onClick={login}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Sign In
          </button>
        )}
      </div>
    </div>
  )
}

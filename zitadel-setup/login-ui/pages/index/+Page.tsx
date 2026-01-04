import React, { useState } from 'react'
import { Logo } from '../../components/Logo'
import { GoogleButton } from '../../components/GoogleButton'
import { Divider } from '../../components/Divider'
import { LoginForm } from '../../components/LoginForm'
import { loginWithGoogle, loginWithPassword } from '../../lib/auth'

export default function LoginPage() {
  const [loading, setLoading] = useState(false)
  const [googleLoading, setGoogleLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGoogleLogin = async () => {
    try {
      setGoogleLoading(true)
      setError(null)
      await loginWithGoogle()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initiate Google login')
      setGoogleLoading(false)
    }
  }

  const handlePasswordLogin = async (email: string, password: string) => {
    try {
      setLoading(true)
      setError(null)
      await loginWithPassword(email, password)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid email or password')
      setLoading(false)
    }
  }

  return (
    <div className="w-full max-w-md">
      {/* Card Container */}
      <div className="card">
        {/* Logo */}
        <div className="mb-8">
          <Logo size="lg" className="mb-4" />
          <h1 className="text-2xl font-bold text-center text-gray-900 dark:text-white">
            Welcome back
          </h1>
          <p className="text-center text-gray-600 dark:text-gray-400 mt-2">
            Sign in to your account to continue
          </p>
        </div>

        {/* Google SSO Button - Primary CTA */}
        <GoogleButton
          onClick={handleGoogleLogin}
          loading={googleLoading}
          disabled={loading}
        />

        {/* Divider */}
        <Divider text="or continue with email" />

        {/* Email/Password Form */}
        <LoginForm
          onSubmit={handlePasswordLogin}
          loading={loading}
          error={error}
        />
      </div>

      {/* Footer */}
      <p className="text-center text-sm text-gray-500 dark:text-gray-400 mt-8">
        By signing in, you agree to our{' '}
        <a href="/terms" className="link">
          Terms of Service
        </a>{' '}
        and{' '}
        <a href="/privacy" className="link">
          Privacy Policy
        </a>
      </p>
    </div>
  )
}

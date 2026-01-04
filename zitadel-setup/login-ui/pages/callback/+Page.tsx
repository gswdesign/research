import React, { useEffect, useState } from 'react'
import { handleCallback } from '../../lib/auth'

export default function CallbackPage() {
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const processCallback = async () => {
      try {
        const user = await handleCallback()

        // Get the return URL from state or default to dashboard
        const returnUrl = sessionStorage.getItem('returnUrl') || '/dashboard'
        sessionStorage.removeItem('returnUrl')

        // Redirect to the application
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
      <div className="w-full max-w-md">
        <div className="card text-center">
          <div className="mb-4">
            <svg
              className="mx-auto h-12 w-12 text-red-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            Authentication Failed
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            {error}
          </p>
          <a href="/" className="btn-primary inline-block">
            Try Again
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full max-w-md">
      <div className="card text-center">
        <div className="mb-4">
          <svg
            className="animate-spin mx-auto h-12 w-12 text-primary-600"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        </div>
        <h1 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
          Completing sign in...
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Please wait while we redirect you.
        </p>
      </div>
    </div>
  )
}

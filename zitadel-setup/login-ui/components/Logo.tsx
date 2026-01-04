import React from 'react'

interface LogoProps {
  className?: string
  size?: 'sm' | 'md' | 'lg'
}

export function Logo({ className = '', size = 'md' }: LogoProps) {
  const sizeClasses = {
    sm: 'h-8 w-auto',
    md: 'h-12 w-auto',
    lg: 'h-16 w-auto',
  }

  return (
    <div className={`flex items-center justify-center ${className}`}>
      {/* Replace with your actual logo */}
      <svg
        className={sizeClasses[size]}
        viewBox="0 0 200 50"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Placeholder logo - replace with your brand */}
        <rect
          x="5"
          y="5"
          width="40"
          height="40"
          rx="8"
          className="fill-primary-600"
        />
        <text
          x="55"
          y="35"
          className="fill-gray-900 dark:fill-white"
          style={{ fontSize: '24px', fontWeight: 600, fontFamily: 'Inter, sans-serif' }}
        >
          YourBrand
        </text>
      </svg>
    </div>
  )
}

export default Logo

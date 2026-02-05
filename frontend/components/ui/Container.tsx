import React from 'react'
import { cn } from '@/lib/utils'

interface ContainerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  children: React.ReactNode
  className?: string
}

export function Container({
  size = 'xl',
  children,
  className
}: ContainerProps) {
  const sizeStyles = {
    sm: 'max-w-screen-sm',   // 640px
    md: 'max-w-screen-md',   // 768px
    lg: 'max-w-screen-lg',   // 1024px
    xl: 'max-w-screen-xl',   // 1280px
    full: 'max-w-full'       // 100%
  }

  return (
    <div
      className={cn(
        'mx-auto px-4 md:px-6 lg:px-8',
        sizeStyles[size],
        className
      )}
    >
      {children}
    </div>
  )
}

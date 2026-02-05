import React from 'react'
import { cn } from '@/lib/utils'

interface SectionProps {
  spacing?: 'sm' | 'md' | 'lg'
  background?: 'white' | 'gray' | 'primary'
  children: React.ReactNode
  className?: string
  id?: string
}

export function Section({
  spacing = 'md',
  background = 'white',
  children,
  className,
  id
}: SectionProps) {
  const spacingStyles = {
    sm: 'py-6 md:py-8',
    md: 'py-8 md:py-12 lg:py-16',
    lg: 'py-12 md:py-16 lg:py-20'
  }

  const backgroundStyles = {
    white: 'bg-white dark:bg-gray-900',
    gray: 'bg-gray-50 dark:bg-gray-800',
    primary: 'bg-primary-50 dark:bg-primary-900/20'
  }

  return (
    <section
      id={id}
      className={cn(
        spacingStyles[spacing],
        backgroundStyles[background],
        className
      )}
    >
      {children}
    </section>
  )
}

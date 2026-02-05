import React from 'react'
import Link from 'next/link'
import { Container } from '@/components/ui/Container'

interface CTAButton {
  text: string
  href: string
}

interface HeroSectionProps {
  title: string
  subtitle: string
  primaryCTA: CTAButton
  secondaryCTA: CTAButton
}

export function HeroSection({
  title,
  subtitle,
  primaryCTA,
  secondaryCTA
}: HeroSectionProps) {
  return (
    <section className="relative overflow-hidden bg-white dark:bg-gray-900">
      {/* Gradient mesh background */}
      <div
        className="absolute inset-0 bg-gradient-mesh opacity-100 dark:opacity-40"
        style={{
          background: `
            radial-gradient(at 20% 30%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
            radial-gradient(at 80% 70%, rgba(139, 92, 246, 0.3) 0%, transparent 50%),
            radial-gradient(at 50% 50%, rgba(59, 130, 246, 0.15) 0%, transparent 60%)
          `
        }}
      />

      {/* Content */}
      <Container>
        <div className="relative text-center flex flex-col items-center py-16 md:py-20 lg:py-24">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white max-w-3xl mx-auto">
            {title}
          </h1>
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 mt-6 max-w-2xl">
            {subtitle}
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 mt-10">
            <Link
              href={primaryCTA.href}
              className="px-8 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-500 dark:bg-primary-500 dark:hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors shadow-lg hover:shadow-xl"
            >
              {primaryCTA.text}
            </Link>
            <Link
              href={secondaryCTA.href}
              className="px-8 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 font-medium rounded-lg border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
            >
              {secondaryCTA.text}
            </Link>
          </div>
        </div>
      </Container>
    </section>
  )
}

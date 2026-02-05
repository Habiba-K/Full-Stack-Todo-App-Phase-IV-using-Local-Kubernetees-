import React from 'react'
import Link from 'next/link'
import { Container } from '@/components/ui/Container'

interface CTASectionProps {
  title: string
  subtitle: string
  ctaText: string
  ctaHref: string
}

export function CTASection({
  title,
  subtitle,
  ctaText,
  ctaHref
}: CTASectionProps) {
  return (
    <section className="relative overflow-hidden">
      {/* Gradient background */}
      <div className="bg-linear-to-r from-primary-500 to-accent-500 dark:from-primary-600 dark:to-accent-600">
        <Container>
          <div className="text-center flex flex-col items-center py-16 md:py-20">
            <h2 className="text-3xl md:text-4xl font-bold text-white max-w-3xl">
              {title}
            </h2>
            <p className="text-lg md:text-xl text-white/90 mt-4 max-w-2xl">
              {subtitle}
            </p>
            <Link
              href={ctaHref}
              className="mt-8 px-8 py-3 bg-white text-primary-600 font-medium rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-primary-600 transition-colors shadow-lg hover:shadow-xl"
            >
              {ctaText}
            </Link>
          </div>
        </Container>
      </div>
    </section>
  )
}

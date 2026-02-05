'use client'

import { ThemeProvider } from '@/components/providers/ThemeProvider'
import { Footer } from '@/components/layout/Footer'

export function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <div className="min-h-screen flex flex-col bg-white dark:bg-gray-950">
        {children}
        <Footer />
      </div>
    </ThemeProvider>
  )
}

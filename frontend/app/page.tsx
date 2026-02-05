import { redirect } from 'next/navigation'
import { getSession } from '@/lib/auth'
import { Container } from '@/components/ui/Container'
import { Section } from '@/components/ui/Section'
import { FeatureCard } from '@/components/homepage/FeatureCard'
import { HeroSection } from '@/components/homepage/HeroSection'
import { CTASection } from '@/components/homepage/CTASection'
import { Navbar } from '@/components/layout/Navbar'
import { Footer } from '@/components/layout/Footer'
import AnimatedSection from '@/components/ui/AnimatedSection'

export default async function HomePage() {
  // Auth check - redirect authenticated users to dashboard
  const session = await getSession()

  if (session?.session?.token) {
    redirect('/dashboard')
  }

  return (
    <div className="min-h-screen flex flex-col bg-white dark:bg-gray-950">
      <Navbar />

      <main className="grow">
        {/* Hero Section with Gradient Mesh - T069: Add entrance animation */}
        <AnimatedSection>
          <HeroSection
            title="Organize Your Life, One Task at a Time"
            subtitle="The simple, powerful todo app that helps you stay focused and get things done."
            primaryCTA={{ text: "Get Started Free", href: "/signup" }}
            secondaryCTA={{ text: "Sign In", href: "/signin" }}
          />
        </AnimatedSection>

        {/* Features Section */}
        <Section id="features" spacing="lg" background="gray">
          <Container>
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
              Everything you need to stay organized
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* T070: Add staggered entrance animations to feature cards */}
              <AnimatedSection delay={100}>
                <FeatureCard
                  icon="✓"
                  title="Simple Task Management"
                  description="Add, complete, and organize your todos with ease. No complicated setup required."
                />
              </AnimatedSection>
              <AnimatedSection delay={200}>
                <FeatureCard
                  icon="📱"
                  title="Access Anywhere"
                  description="Your tasks sync across all devices. Start on your phone, continue on desktop."
                />
              </AnimatedSection>
              <AnimatedSection delay={300}>
                <FeatureCard
                  icon="🔒"
                  title="Secure & Private"
                  description="Your data is encrypted and private. Only you can see your tasks."
                />
              </AnimatedSection>
            </div>
          </Container>
        </Section>

        {/* Bottom CTA Section with Gradient - T071: Add entrance animation */}
        <AnimatedSection>
          <CTASection
            title="Ready to get organized?"
            subtitle="Join thousands of users who stay productive every day."
            ctaText="Get Started Free"
            ctaHref="/signup"
          />
        </AnimatedSection>
      </main>
    </div>
  )
}


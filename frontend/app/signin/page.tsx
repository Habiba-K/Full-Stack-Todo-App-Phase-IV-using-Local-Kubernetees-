import Link from 'next/link'
import { SigninForm } from '@/components/auth/SigninForm'
import { Card } from '@/components/ui/Card'

export default function SigninPage() {
  return (
    <div className="bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-8 md:py-12">
      <div className="w-full max-w-md">
        <Link
          href="/"
          className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 mb-6 inline-flex items-center transition-colors"
        >
          ← Back to Home
        </Link>
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome Back
          </h1>
          <p className="text-base text-gray-600 dark:text-gray-400">
            Sign in to access your tasks
          </p>
        </div>

        <Card>
          <SigninForm />

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Don't have an account?{' '}
              <Link
                href="/signup"
                className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-500 font-medium"
              >
                Sign up
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  )
}

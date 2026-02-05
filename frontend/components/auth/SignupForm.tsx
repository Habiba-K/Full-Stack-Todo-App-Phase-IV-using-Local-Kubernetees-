'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { SignupRequest } from '@/types'
import { setSession } from '@/lib/auth'

interface SignupFormProps {
  onSuccess?: () => void
}

export function SignupForm({ onSuccess }: SignupFormProps) {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<SignupRequest>()

  const onSubmit = async (data: SignupRequest) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))

        if (response.status === 409) {
          throw new Error('An account with this email already exists')
        }

        if (response.status === 422) {
          throw new Error(errorData.detail || 'Invalid input. Please check your information.')
        }

        throw new Error(errorData.detail || 'Failed to create account')
      }

      const result = await response.json()

      // If backend returns token and user, set session and redirect to dashboard
      // Otherwise, redirect to signin page
      if (result.token && result.user) {
        setSession(result.token, result.user)
        if (onSuccess) {
          onSuccess()
        } else {
          router.push('/dashboard')
        }
      } else {
        // Redirect to signin page
        if (onSuccess) {
          onSuccess()
        } else {
          router.push('/signin')
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        label="Email"
        type="email"
        {...register('email', {
          required: 'Email is required',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'Invalid email address'
          }
        })}
        error={errors.email?.message}
        disabled={loading}
      />

      <Input
        label="Password"
        type="password"
        {...register('password', {
          required: 'Password is required',
          minLength: {
            value: 8,
            message: 'Password must be at least 8 characters'
          }
        })}
        error={errors.password?.message}
        helperText="Minimum 8 characters"
        disabled={loading}
      />

      <Input
        label="Name (optional)"
        type="text"
        {...register('name', {
          maxLength: {
            value: 100,
            message: 'Name must be less than 100 characters'
          }
        })}
        error={errors.name?.message}
        disabled={loading}
      />

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}

      <Button
        type="submit"
        variant="primary"
        fullWidth
        loading={loading}
        disabled={loading}
      >
        Create Account
      </Button>
    </form>
  )
}

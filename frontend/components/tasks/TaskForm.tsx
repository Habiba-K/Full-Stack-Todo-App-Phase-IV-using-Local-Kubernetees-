'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { CreateTaskRequest, UpdateTaskRequest, Task } from '@/types'

interface TaskFormProps {
  task?: Task // Optional for edit mode
  onSubmit: (data: CreateTaskRequest | UpdateTaskRequest) => Promise<void>
  onSuccess?: () => void
  onCancel?: () => void
  loading?: boolean
}

export function TaskForm({ task, onSubmit, onSuccess, onCancel, loading: externalLoading }: TaskFormProps) {
  const [error, setError] = useState<string | null>(null)
  const [internalLoading, setInternalLoading] = useState(false)

  const loading = externalLoading || internalLoading
  const isEditMode = !!task

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<CreateTaskRequest>({
    defaultValues: task ? {
      title: task.title,
      description: task.description || ''
    } : undefined
  })

  // Update form when task prop changes
  useEffect(() => {
    if (task) {
      reset({
        title: task.title,
        description: task.description || ''
      })
    }
  }, [task, reset])

  const handleFormSubmit = async (data: CreateTaskRequest) => {
    setInternalLoading(true)
    setError(null)

    try {
      await onSubmit(data)
      if (!isEditMode) {
        reset() // Reset form after successful creation
      }
      if (onSuccess) {
        onSuccess()
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to ${isEditMode ? 'update' : 'create'} task`)
    } finally {
      setInternalLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
      <Input
        label="Task Title"
        placeholder="What needs to be done?"
        {...register('title', {
          required: 'Title is required',
          maxLength: {
            value: 200,
            message: 'Title must be less than 200 characters'
          }
        })}
        error={errors.title?.message}
        disabled={loading}
      />

      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          Description (optional)
        </label>
        <textarea
          id="description"
          rows={3}
          placeholder="Add more details..."
          {...register('description', {
            maxLength: {
              value: 1000,
              message: 'Description must be less than 1000 characters'
            }
          })}
          disabled={loading}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors resize-none"
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.description.message}</p>
        )}
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}

      <div className="flex gap-3">
        <Button
          type="submit"
          variant="primary"
          fullWidth={!isEditMode}
          loading={loading}
          disabled={loading}
        >
          {isEditMode ? 'Save Changes' : 'Add Task'}
        </Button>

        {isEditMode && onCancel && (
          <Button
            type="button"
            variant="secondary"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </Button>
        )}
      </div>
    </form>
  )
}

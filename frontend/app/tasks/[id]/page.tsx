'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { Task } from '@/types'
import { Card } from '@/components/ui/Card'
import { Loading } from '@/components/ui/Loading'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { Button } from '@/components/ui/Button'
import { ConfirmDialog } from '@/components/ui/ConfirmDialog'
import { api } from '@/lib/api-client'
import { getSession } from '@/lib/auth'
import { formatDate, formatRelativeTime } from '@/lib/utils'

export default function TaskDetailPage() {
  const router = useRouter()
  const params = useParams()
  const taskId = params.id as string

  const [task, setTask] = useState<Task | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [userId, setUserId] = useState<string | null>(null)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [deleteLoading, setDeleteLoading] = useState(false)

  // Fetch task details
  useEffect(() => {
    const fetchTask = async () => {
      try {
        setLoading(true)
        setError(null)

        // Get session to extract user_id
        const session = await getSession()

        if (!session?.session?.token) {
          router.push('/signin')
          return
        }

        const user = session.user
        if (!user?.id) {
          throw new Error('User ID not found in session')
        }

        setUserId(user.id)

        // Fetch task details
        const fetchedTask = await api.get<Task>(`/api/${user.id}/tasks/${taskId}`)
        setTask(fetchedTask)
      } catch (err) {
        if (err instanceof Error) {
          if (err.message.includes('404') || err.message.includes('not found')) {
            setError('Task not found. It may have been deleted.')
          } else {
            setError(err.message)
          }
        } else {
          setError('Failed to load task')
        }
      } finally {
        setLoading(false)
      }
    }

    fetchTask()
  }, [taskId, router])

  const handleEdit = () => {
    router.push(`/tasks/${taskId}/edit`)
  }

  const handleDelete = () => {
    setDeleteDialogOpen(true)
  }

  const confirmDelete = async () => {
    if (!userId || !taskId) return

    setDeleteLoading(true)

    try {
      await api.delete(`/api/${userId}/tasks/${taskId}`)
      router.push('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task')
      setDeleteDialogOpen(false)
    } finally {
      setDeleteLoading(false)
    }
  }

  const cancelDelete = () => {
    setDeleteDialogOpen(false)
  }

  const handleBack = () => {
    router.push('/dashboard')
  }

  const handleRetry = () => {
    window.location.reload()
  }

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loading />
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <h1 className="text-2xl font-bold text-gray-900">Task Details</h1>
          </div>
        </header>

        <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <ErrorMessage
            message={error}
            onRetry={handleRetry}
            onCancel={handleBack}
          />
        </main>
      </div>
    )
  }

  // Task not found
  if (!task) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <h1 className="text-2xl font-bold text-gray-900">Task Details</h1>
          </div>
        </header>

        <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Card>
            <p className="text-gray-600">Task not found.</p>
            <button
              onClick={handleBack}
              className="mt-4 text-primary-600 hover:text-primary-700"
            >
              ← Back to Dashboard
            </button>
          </Card>
        </main>
      </div>
    )
  }

  // Render task details
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={handleBack}
              className="text-gray-600 hover:text-gray-900"
              title="Back to dashboard"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 19l-7-7m0 0l7-7m-7 7h18"
                />
              </svg>
            </button>
            <h1 className="text-2xl font-bold text-gray-900">Task Details</h1>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          {/* Task status badge */}
          <div className="mb-4">
            {task.completed ? (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                ✓ Completed
              </span>
            ) : (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                ⏳ Pending
              </span>
            )}
          </div>

          {/* Task title */}
          <h2
            className={`text-2xl font-bold mb-4 ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}
          >
            {task.title}
          </h2>

          {/* Task description */}
          {task.description && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Description</h3>
              <p className="text-gray-600 whitespace-pre-wrap">{task.description}</p>
            </div>
          )}

          {/* Task metadata */}
          <div className="border-t border-gray-200 pt-4 mb-6">
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <dt className="text-sm font-medium text-gray-500">Created</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {formatDate(task.created_at)}
                  <span className="text-gray-500 ml-2">
                    ({formatRelativeTime(task.created_at)})
                  </span>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {formatDate(task.updated_at)}
                  <span className="text-gray-500 ml-2">
                    ({formatRelativeTime(task.updated_at)})
                  </span>
                </dd>
              </div>
            </dl>
          </div>

          {/* Action buttons */}
          <div className="flex gap-3">
            <Button
              variant="primary"
              onClick={handleEdit}
            >
              Edit Task
            </Button>
            <Button
              variant="danger"
              onClick={handleDelete}
            >
              Delete Task
            </Button>
          </div>
        </Card>
      </main>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Delete Task"
        message="Are you sure you want to delete this task? This action cannot be undone."
        confirmLabel="Delete"
        cancelLabel="Cancel"
        variant="danger"
        loading={deleteLoading}
        onConfirm={confirmDelete}
        onCancel={cancelDelete}
      />
    </div>
  )
}

'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { Task, UpdateTaskRequest } from '@/types'
import { TaskForm } from '@/components/tasks/TaskForm'
import { Card } from '@/components/ui/Card'
import { Loading } from '@/components/ui/Loading'
import { ErrorMessage } from '@/components/ui/ErrorMessage'
import { api } from '@/lib/api-client'
import { getSession } from '@/lib/auth'

export default function EditTaskPage() {
  const router = useRouter()
  const params = useParams()
  const taskId = params.id as string

  const [task, setTask] = useState<Task | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [userId, setUserId] = useState<string | null>(null)
  const [updateLoading, setUpdateLoading] = useState(false)

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
          // Handle 404 - task not found
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

  const handleUpdateTask = async (data: UpdateTaskRequest) => {
    if (!userId || !taskId) {
      throw new Error('Missing user ID or task ID')
    }

    setUpdateLoading(true)

    try {
      // Update task via API
      await api.put<Task>(`/api/${userId}/tasks/${taskId}`, data)

      // Redirect to dashboard on success
      router.push('/dashboard')
    } catch (err) {
      setUpdateLoading(false)
      throw err // Let TaskForm handle the error
    }
  }

  const handleCancel = () => {
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
            <h1 className="text-2xl font-bold text-gray-900">Edit Task</h1>
          </div>
        </header>

        <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <ErrorMessage
            message={error}
            onRetry={handleRetry}
            onCancel={handleCancel}
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
            <h1 className="text-2xl font-bold text-gray-900">Edit Task</h1>
          </div>
        </header>

        <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Card>
            <p className="text-gray-600">Task not found.</p>
            <button
              onClick={handleCancel}
              className="mt-4 text-primary-600 hover:text-primary-700"
            >
              ← Back to Dashboard
            </button>
          </Card>
        </main>
      </div>
    )
  }

  // Render edit form
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={handleCancel}
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
            <h1 className="text-2xl font-bold text-gray-900">Edit Task</h1>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Update Task Details
          </h2>
          <TaskForm
            task={task}
            onSubmit={handleUpdateTask}
            onCancel={handleCancel}
            loading={updateLoading}
          />
        </Card>
      </main>
    </div>
  )
}

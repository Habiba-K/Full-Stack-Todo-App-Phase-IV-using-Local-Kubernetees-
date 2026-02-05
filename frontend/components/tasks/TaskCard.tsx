'use client'

import { useRouter } from 'next/navigation'
import { Task } from '@/types'
import { Card } from '@/components/ui/Card'
import { formatRelativeTime } from '@/lib/utils'

interface TaskCardProps {
  task: Task
  onToggleComplete?: (taskId: string) => Promise<void>
  onEdit?: (taskId: string) => void
  onDelete?: (taskId: string) => Promise<void>
}

export function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const router = useRouter()

  const handleCardClick = (e: React.MouseEvent) => {
    // Don't navigate if clicking on interactive elements
    const target = e.target as HTMLElement
    if (
      target.tagName === 'INPUT' ||
      target.tagName === 'BUTTON' ||
      target.closest('button') ||
      target.closest('input')
    ) {
      return
    }
    router.push(`/tasks/${task.id}`)
  }

  return (
    <Card
      className="hover:shadow-lg dark:hover:shadow-xl transition-all duration-200 cursor-pointer"
      onClick={handleCardClick}
    >
      <div className="flex items-start gap-3">
        {/* Completion checkbox */}
        <div className="flex-shrink-0 mt-1">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggleComplete?.(task.id)}
            className="w-5 h-5 rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-400 cursor-pointer dark:bg-gray-700"
          />
        </div>

        {/* Task content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-semibold ${
              task.completed
                ? 'line-through text-gray-500 dark:text-gray-500'
                : 'text-gray-900 dark:text-white'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
              {task.description}
            </p>
          )}

          <div className="mt-3 flex items-center gap-4 text-xs text-gray-500 dark:text-gray-500">
            <span>
              Created {formatRelativeTime(task.created_at)}
            </span>
            {task.completed && (
              <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400 font-medium">
                ✓ Completed
              </span>
            )}
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex-shrink-0 flex gap-2">
          {onEdit && (
            <button
              onClick={() => onEdit(task.id)}
              className="text-gray-400 dark:text-gray-500 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
              title="Edit task"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </button>
          )}

          {onDelete && (
            <button
              onClick={() => onDelete(task.id)}
              className="text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 transition-colors"
              title="Delete task"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          )}
        </div>
      </div>
    </Card>
  )
}

import React from 'react'
import { Button } from './Button'

interface ErrorMessageProps {
  message: string
  onRetry?: () => void
  onCancel?: () => void
}

export function ErrorMessage({ message, onRetry, onCancel }: ErrorMessageProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 max-w-md w-full">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <svg
              className="h-6 w-6 text-red-600 dark:text-red-400"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div className="ml-3 flex-1">
            <h3 className="text-sm font-medium text-red-800 dark:text-red-300">Error</h3>
            <p className="mt-2 text-sm text-red-700 dark:text-red-400">{message}</p>
            {(onRetry || onCancel) && (
              <div className="mt-4 flex gap-2">
                {onRetry && (
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={onRetry}
                  >
                    Try Again
                  </Button>
                )}
                {onCancel && (
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={onCancel}
                  >
                    Go Back
                  </Button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

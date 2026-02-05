'use client';

import { Suspense } from 'react';
import ChatContainer from '@/components/chat/ChatContainer';
import Link from 'next/link';

// Loading skeleton component
function ChatSkeleton() {
  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg animate-pulse">
      <div className="flex-1 p-4 space-y-4">
        <div className="flex justify-end">
          <div className="w-2/3 h-16 bg-gray-200 rounded-lg"></div>
        </div>
        <div className="flex justify-start">
          <div className="w-3/4 h-20 bg-gray-200 rounded-lg"></div>
        </div>
        <div className="flex justify-end">
          <div className="w-1/2 h-12 bg-gray-200 rounded-lg"></div>
        </div>
      </div>
      <div className="border-t border-gray-200 p-4">
        <div className="h-10 bg-gray-200 rounded-lg"></div>
      </div>
    </div>
  );
}

// Error boundary fallback
function ChatError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="text-red-500 mb-4">
            <svg
              className="w-16 h-16 mx-auto"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Something went wrong
          </h2>
          <p className="text-gray-600 mb-6">
            {error.message || 'Failed to load the chat interface. Please try again.'}
          </p>
          <button
            onClick={reset}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  );
}

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link
                href="/dashboard"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                ← Back to Dashboard
              </Link>
              <h1 className="text-2xl font-bold text-gray-900">AI Task Assistant</h1>
            </div>
            <Link
              href="/dashboard"
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
            >
              View Tasks
            </Link>
          </div>
        </div>
      </header>

      {/* Chat Container with Error Boundary */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="h-[calc(100vh-12rem)]">
          <Suspense fallback={<ChatSkeleton />}>
            <ChatContainer />
          </Suspense>
        </div>
      </main>
    </div>
  );
}


// Task entity type
export interface Task {
  id: string // UUID
  user_id: string // UUID
  title: string
  description: string | null
  completed: boolean
  created_at: string // ISO 8601 datetime
  updated_at: string // ISO 8601 datetime
}

// Task operation types
export interface CreateTaskRequest {
  title: string
  description?: string
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
  completed?: boolean
}

// Task list response
export type TaskListResponse = Task[]

// UI state types
export interface LoadingState {
  isLoading: boolean
  message?: string
}

export interface ErrorState {
  hasError: boolean
  message: string
  code?: string // 'UNAUTHORIZED' | 'FORBIDDEN' | 'NOT_FOUND' | 'SERVER_ERROR'
}

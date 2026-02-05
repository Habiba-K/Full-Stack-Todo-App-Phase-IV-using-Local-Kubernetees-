# Data Model: Frontend UI + API Integration

**Feature**: 002-frontend-todo-ui
**Date**: 2026-01-23
**Status**: Complete

## Overview

This document defines the TypeScript types, interfaces, and data structures used in the Next.js frontend application. These types mirror the backend API contracts and provide type safety throughout the application.

## Frontend Data Entities

### User Entity

**Purpose**: Represents an authenticated user in the application.

**TypeScript Interface**:

```typescript
export interface User {
  id: string // UUID
  email: string
  name: string | null
  created_at: string // ISO 8601 datetime
  updated_at: string // ISO 8601 datetime
}
```

**Usage**:
- Stored in AuthContext after successful signin
- Displayed in user profile/header
- Used to derive user_id for API calls

**Validation Rules**:
- id: Valid UUID format
- email: Valid email format (validated by backend)
- name: Optional, 1-100 characters if provided

---

### Task Entity

**Purpose**: Represents a todo task item.

**TypeScript Interface**:

```typescript
export interface Task {
  id: string // UUID
  user_id: string // UUID
  title: string
  description: string | null
  completed: boolean
  created_at: string // ISO 8601 datetime
  updated_at: string // ISO 8601 datetime
}
```

**Usage**:
- Fetched from GET /api/{user_id}/tasks
- Displayed in TaskList and TaskCard components
- Updated via PUT /api/{user_id}/tasks/{id}

**Validation Rules**:
- id: Valid UUID format
- user_id: Must match authenticated user
- title: Required, 1-200 characters
- description: Optional, max 1000 characters
- completed: Boolean (true/false)

**Display Formatting**:
- completed: Show checkmark or strikethrough
- created_at: Format as "Jan 23, 2026" or relative time
- updated_at: Show "Last updated X ago" if recent

---

### Authentication Types

**Signup Request**:

```typescript
export interface SignupRequest {
  email: string
  password: string
  name?: string
}
```

**Signin Request**:

```typescript
export interface SigninRequest {
  email: string
  password: string
}
```

**Auth Response**:

```typescript
export interface AuthResponse {
  user: User
  token: string
  expires_at: string
}
```

**Session State**:

```typescript
export interface SessionState {
  user: User | null
  token: string | null
  loading: boolean
  error: string | null
}
```

---

### Task Operation Types

**Create Task Request**:

```typescript
export interface CreateTaskRequest {
  title: string
  description?: string
}
```

**Update Task Request**:

```typescript
export interface UpdateTaskRequest {
  title?: string
  description?: string
  completed?: boolean
}
```

**Task List Response**:

```typescript
export type TaskListResponse = Task[]
```

---

### UI State Types

**Loading State**:

```typescript
export interface LoadingState {
  isLoading: boolean
  message?: string
}
```

**Error State**:

```typescript
export interface ErrorState {
  hasError: boolean
  message: string
  code?: string // 'UNAUTHORIZED' | 'FORBIDDEN' | 'NOT_FOUND' | 'SERVER_ERROR'
}
```

**Form State** (React Hook Form):

```typescript
export interface FormState<T> {
  values: T
  errors: Partial<Record<keyof T, string>>
  isSubmitting: boolean
  isValid: boolean
}
```

**API Response Wrapper**:

```typescript
export interface ApiResponse<T> {
  data: T | null
  error: ErrorState | null
  loading: boolean
}
```

---

## State Management Patterns

### Authentication Context

**Context Type**:

```typescript
export interface AuthContextType {
  user: User | null
  loading: boolean
  error: string | null
  signin: (credentials: SigninRequest) => Promise<void>
  signup: (data: SignupRequest) => Promise<void>
  signout: () => Promise<void>
  refreshSession: () => Promise<void>
}
```

**Provider Implementation**:

```typescript
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Implementation details...

  return (
    <AuthContext.Provider value={{ user, loading, error, signin, signup, signout, refreshSession }}>
      {children}
    </AuthContext.Provider>
  )
}
```

### Component State Pattern

**Task List Component State**:

```typescript
interface TaskListState {
  tasks: Task[]
  loading: boolean
  error: string | null
  filter: 'all' | 'pending' | 'completed'
}

const [state, setState] = useState<TaskListState>({
  tasks: [],
  loading: true,
  error: null,
  filter: 'all'
})
```

**Task Form Component State**:

```typescript
interface TaskFormState {
  title: string
  description: string
  submitting: boolean
  error: string | null
}
```

---

## API Client Types

**API Client Configuration**:

```typescript
export interface ApiClientConfig {
  baseURL: string
  timeout?: number
  headers?: Record<string, string>
}
```

**API Error**:

```typescript
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}
```

**API Methods**:

```typescript
export interface ApiClient {
  get<T>(endpoint: string): Promise<T>
  post<T>(endpoint: string, data: any): Promise<T>
  put<T>(endpoint: string, data: any): Promise<T>
  delete<T>(endpoint: string): Promise<T>
  patch<T>(endpoint: string, data?: any): Promise<T>
}
```

---

## Form Validation Schemas

**Signup Form Validation**:

```typescript
export const signupSchema = {
  email: {
    required: 'Email is required',
    pattern: {
      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
      message: 'Invalid email address'
    }
  },
  password: {
    required: 'Password is required',
    minLength: {
      value: 8,
      message: 'Password must be at least 8 characters'
    }
  },
  name: {
    maxLength: {
      value: 100,
      message: 'Name must be less than 100 characters'
    }
  }
}
```

**Task Form Validation**:

```typescript
export const taskSchema = {
  title: {
    required: 'Title is required',
    maxLength: {
      value: 200,
      message: 'Title must be less than 200 characters'
    }
  },
  description: {
    maxLength: {
      value: 1000,
      message: 'Description must be less than 1000 characters'
    }
  }
}
```

---

## Component Props Types

**TaskCard Props**:

```typescript
export interface TaskCardProps {
  task: Task
  onToggleComplete: (taskId: string) => Promise<void>
  onEdit: (taskId: string) => void
  onDelete: (taskId: string) => Promise<void>
}
```

**TaskList Props**:

```typescript
export interface TaskListProps {
  tasks: Task[]
  loading: boolean
  error: string | null
  onCreateTask: (data: CreateTaskRequest) => Promise<void>
  onToggleComplete: (taskId: string) => Promise<void>
  onDeleteTask: (taskId: string) => Promise<void>
}
```

**TaskForm Props**:

```typescript
export interface TaskFormProps {
  task?: Task // Optional for edit mode
  onSubmit: (data: CreateTaskRequest | UpdateTaskRequest) => Promise<void>
  onCancel: () => void
  loading?: boolean
}
```

**Button Props**:

```typescript
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  fullWidth?: boolean
}
```

**Input Props**:

```typescript
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
}
```

---

## Utility Types

**Async State**:

```typescript
export type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
```

**Pagination** (future enhancement):

```typescript
export interface PaginationState {
  page: number
  pageSize: number
  total: number
  hasNext: boolean
  hasPrevious: boolean
}
```

**Filter Options**:

```typescript
export type TaskFilter = 'all' | 'pending' | 'completed'

export interface FilterState {
  filter: TaskFilter
  sortBy?: 'created_at' | 'updated_at' | 'title'
  sortOrder?: 'asc' | 'desc'
}
```

---

## Type Guards

**User Type Guard**:

```typescript
export function isUser(value: any): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof value.id === 'string' &&
    typeof value.email === 'string'
  )
}
```

**Task Type Guard**:

```typescript
export function isTask(value: any): value is Task {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof value.id === 'string' &&
    typeof value.title === 'string' &&
    typeof value.completed === 'boolean'
  )
}
```

**API Error Type Guard**:

```typescript
export function isApiError(error: any): error is ApiError {
  return error instanceof ApiError
}
```

---

## Constants

**API Endpoints**:

```typescript
export const API_ENDPOINTS = {
  AUTH: {
    SIGNUP: '/api/auth/signup',
    SIGNIN: '/api/auth/signin',
    LOGOUT: '/api/auth/logout',
    ME: '/api/auth/me'
  },
  TASKS: {
    LIST: (userId: string) => `/api/${userId}/tasks`,
    CREATE: (userId: string) => `/api/${userId}/tasks`,
    DETAIL: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}`,
    UPDATE: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}`,
    DELETE: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}`,
    TOGGLE: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}/complete`
  }
} as const
```

**Error Messages**:

```typescript
export const ERROR_MESSAGES = {
  UNAUTHORIZED: 'Please sign in to continue',
  FORBIDDEN: 'You do not have permission to perform this action',
  NOT_FOUND: 'The requested resource was not found',
  SERVER_ERROR: 'An unexpected error occurred. Please try again later',
  NETWORK_ERROR: 'Unable to connect to the server. Please check your internet connection'
} as const
```

**Validation Messages**:

```typescript
export const VALIDATION_MESSAGES = {
  REQUIRED: (field: string) => `${field} is required`,
  MIN_LENGTH: (field: string, length: number) => `${field} must be at least ${length} characters`,
  MAX_LENGTH: (field: string, length: number) => `${field} must be less than ${length} characters`,
  INVALID_EMAIL: 'Please enter a valid email address',
  INVALID_FORMAT: (field: string) => `${field} format is invalid`
} as const
```

---

## Type Exports

**Central Type Export** (types/index.ts):

```typescript
// User types
export type { User, SessionState, AuthContextType }
export type { SignupRequest, SigninRequest, AuthResponse }

// Task types
export type { Task, CreateTaskRequest, UpdateTaskRequest, TaskListResponse }

// UI types
export type { LoadingState, ErrorState, ApiResponse, AsyncState }

// Component props
export type { TaskCardProps, TaskListProps, TaskFormProps }
export type { ButtonProps, InputProps }

// API types
export type { ApiClient, ApiClientConfig, ApiError }

// Utility types
export type { TaskFilter, FilterState }

// Constants
export { API_ENDPOINTS, ERROR_MESSAGES, VALIDATION_MESSAGES }

// Type guards
export { isUser, isTask, isApiError }
```

---

## Migration from Backend Types

**Backend to Frontend Mapping**:

| Backend Field | Frontend Field | Transformation |
|---------------|----------------|----------------|
| id (UUID) | id (string) | Direct mapping |
| created_at (datetime) | created_at (string) | ISO 8601 string |
| updated_at (datetime) | updated_at (string) | ISO 8601 string |
| user_id (UUID) | user_id (string) | Direct mapping |
| completed (bool) | completed (boolean) | Direct mapping |

**Date Formatting Utilities**:

```typescript
export function formatDate(isoString: string): string {
  return new Date(isoString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

export function formatRelativeTime(isoString: string): string {
  const date = new Date(isoString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)

  if (diffMins < 1) return 'just now'
  if (diffMins < 60) return `${diffMins} minutes ago`
  if (diffMins < 1440) return `${Math.floor(diffMins / 60)} hours ago`
  return formatDate(isoString)
}
```

---

## Summary

This data model provides:
- **Type Safety**: TypeScript interfaces for all entities
- **Validation**: Schema definitions for forms
- **Error Handling**: Structured error types
- **Component Props**: Typed props for all components
- **API Integration**: Types matching backend contracts
- **Utility Functions**: Type guards and formatters

All types are exported from a central location for easy imports throughout the application.

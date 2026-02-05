// User entity types
export interface User {
  id: string // UUID
  email: string
  name: string | null
  created_at: string // ISO 8601 datetime
  updated_at: string // ISO 8601 datetime
}

// Authentication request types
export interface SignupRequest {
  email: string
  password: string
  name?: string
}

export interface SigninRequest {
  email: string
  password: string
}

// Authentication response types
export interface AuthResponse {
  user: User
  token: string
  expires_at: string
}

// Session state
export interface SessionState {
  user: User | null
  token: string | null
  loading: boolean
  error: string | null
}

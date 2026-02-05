# Research: Frontend UI + API Integration

**Feature**: 002-frontend-todo-ui
**Date**: 2026-01-23
**Status**: Complete

## Research Task 1: Styling Approach

### Question
Which styling solution should we use for responsive design in Next.js 16+?

### Findings

**Options Evaluated**:

| Solution | Bundle Size | Learning Curve | Responsive Support | Next.js Integration |
|----------|-------------|----------------|-------------------|---------------------|
| Tailwind CSS | Small (with purging) | Medium | Excellent | Native |
| CSS Modules | Minimal | Low | Good | Native |
| styled-components | Medium | Medium | Good | Requires config |

**Tailwind CSS Benefits**:
- Mobile-first responsive utilities (sm:, md:, lg:, xl:)
- Rapid development with utility classes
- Automatic purging removes unused styles
- Excellent documentation and community
- Built-in dark mode support (future enhancement)

**CSS Modules Benefits**:
- Traditional CSS approach
- Scoped styles by default
- No learning curve for CSS developers

**styled-components Benefits**:
- Dynamic styling with props
- CSS-in-JS co-location
- Theme support

### Decision

**Approach**: Tailwind CSS

**Rationale**:
- Best-in-class responsive design utilities
- Fastest development velocity for UI implementation
- Small production bundle with automatic purging
- Perfect fit for mobile-first design requirement
- Industry standard for modern React applications

**Implementation Notes**:
- Configure Tailwind with custom colors and spacing
- Use responsive breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Create custom utility classes for common patterns
- Use @apply directive sparingly for complex components

---

## Research Task 2: State Management

### Question
How should we manage authentication state and task data in the frontend?

### Findings

**State Categories**:
1. **Authentication State**: User info, session, JWT token
2. **Task Data**: Task list, individual task details
3. **UI State**: Loading, error, form state

**Options Evaluated**:

| Solution | Complexity | Bundle Size | Use Case |
|----------|-----------|-------------|----------|
| React Context | Low | 0 KB | Auth state, global config |
| Zustand | Low | 1 KB | Simple global state |
| Redux Toolkit | High | 10+ KB | Complex state management |
| Component State | Minimal | 0 KB | Local UI state |

**React Context Pattern**:
```typescript
// AuthContext for user session
const AuthContext = createContext<AuthState | null>(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  )
}
```

**Component State Pattern**:
```typescript
// Task list in dashboard component
const [tasks, setTasks] = useState<Task[]>([])
const [loading, setLoading] = useState(false)
const [error, setError] = useState<string | null>(null)
```

### Decision

**Approach**: React Context for auth + Component state for tasks

**Rationale**:
- Auth state needs to be accessible across the app (Context)
- Task data is page-specific (Component state)
- No external dependencies required
- Simple mental model for developers
- Sufficient for application complexity

**Implementation Pattern**:
- AuthContext wraps entire app in root layout
- Task data fetched and stored in page components
- UI state (loading, error) managed locally
- Better Auth handles session persistence

**Trade-offs**:
- May need refactoring if state becomes complex
- No built-in caching (acceptable for this use case)
- Manual loading and error state management

---

## Research Task 3: Form Handling

### Question
Which form library should we use for signup, signin, and task forms?

### Findings

**Options Evaluated**:

| Library | Performance | Validation | Bundle Size | TypeScript |
|---------|------------|------------|-------------|------------|
| React Hook Form | Excellent | Built-in | 9 KB | Excellent |
| Formik | Good | Built-in | 13 KB | Good |
| Native Forms | Excellent | Manual | 0 KB | Manual |

**React Hook Form Benefits**:
- Uncontrolled components (minimal re-renders)
- Built-in validation with schema support
- Excellent TypeScript support
- Small bundle size
- Easy error handling

**Example Usage**:
```typescript
const { register, handleSubmit, formState: { errors } } = useForm<SignupForm>()

const onSubmit = async (data: SignupForm) => {
  try {
    await apiClient.signup(data)
    router.push('/dashboard')
  } catch (error) {
    setError(error.message)
  }
}

<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register('email', { required: true })} />
  {errors.email && <span>Email is required</span>}
</form>
```

### Decision

**Approach**: React Hook Form

**Rationale**:
- Best performance for form-heavy application
- Built-in validation reduces boilerplate
- Excellent TypeScript integration
- Small bundle size impact
- Easy integration with API error handling

**Implementation Notes**:
- Use register() for form fields
- Use handleSubmit() for form submission
- Display validation errors inline
- Handle API errors separately from validation errors

---

## Research Task 4: API Client Implementation

### Question
How should we implement the API client with JWT token injection?

### Findings

**Requirements**:
- Inject JWT token from Better Auth session
- Handle 401 (redirect to signin)
- Handle 403 (show error)
- Handle 5xx (show error)
- Support all HTTP methods (GET, POST, PUT, DELETE, PATCH)

**Custom Fetch Wrapper Pattern**:
```typescript
async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const session = await getSession() // Better Auth
  const token = session?.token

  if (!token) {
    redirect('/signin')
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options?.headers
    }
  })

  if (response.status === 401) {
    redirect('/signin')
  }

  if (response.status === 403) {
    throw new Error('Access forbidden')
  }

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'API request failed')
  }

  return response.json()
}
```

**Helper Functions**:
```typescript
export const api = {
  get: <T>(endpoint: string) => apiClient<T>(endpoint),
  post: <T>(endpoint: string, data: any) =>
    apiClient<T>(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  put: <T>(endpoint: string, data: any) =>
    apiClient<T>(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
  delete: <T>(endpoint: string) =>
    apiClient<T>(endpoint, { method: 'DELETE' }),
  patch: <T>(endpoint: string, data?: any) =>
    apiClient<T>(endpoint, { method: 'PATCH', body: data ? JSON.stringify(data) : undefined })
}
```

### Decision

**Approach**: Custom fetch wrapper with helper methods

**Rationale**:
- Full control over error handling
- No additional dependencies
- Easy to integrate with Better Auth
- TypeScript support for response types
- Sufficient for CRUD operations

**Implementation Notes**:
- Create api-client.ts in lib/ directory
- Export helper methods for each HTTP verb
- Handle errors consistently
- Use TypeScript generics for type safety

---

## Research Task 5: Better Auth Configuration

### Question
How should we configure Better Auth for Next.js App Router with JWT tokens?

### Findings

**Better Auth Setup for Next.js**:
```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.NEXTAUTH_URL!,
  database: {
    // Connect to same database as backend
    url: process.env.DATABASE_URL!
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7 // 7 days
    }
  },
  jwt: {
    enabled: true,
    maxAge: 60 * 60 * 24 * 7 // 7 days
  }
})
```

**Session Access Patterns**:

**Server Components**:
```typescript
import { auth } from '@/lib/auth'

export default async function DashboardPage() {
  const session = await auth.api.getSession()

  if (!session) {
    redirect('/signin')
  }

  return <Dashboard user={session.user} />
}
```

**Client Components**:
```typescript
'use client'
import { useSession } from '@/lib/auth'

export function UserProfile() {
  const { data: session, status } = useSession()

  if (status === 'loading') return <Loading />
  if (!session) return null

  return <div>{session.user.email}</div>
}
```

**Token Storage**:
- Better Auth uses httpOnly cookies by default
- Tokens not accessible via JavaScript (XSS protection)
- Automatic token refresh handling
- Works with Server and Client Components

### Decision

**Approach**: Better Auth with httpOnly cookies

**Rationale**:
- Most secure token storage (httpOnly cookies)
- Automatic session management
- Works seamlessly with Next.js App Router
- Handles token refresh automatically
- Industry best practice

**Implementation Notes**:
- Configure Better Auth in lib/auth.ts
- Use auth.api.getSession() in Server Components
- Use useSession() hook in Client Components
- Middleware checks auth state on protected routes

---

## Summary of Decisions

| Research Area | Decision | Key Rationale |
|---------------|----------|---------------|
| Styling | Tailwind CSS | Best responsive utilities, fast development |
| State Management | React Context + Component State | Simple, no dependencies, sufficient complexity |
| Form Handling | React Hook Form | Best performance, built-in validation |
| API Client | Custom fetch wrapper | Full control, no dependencies, TypeScript support |
| Better Auth | httpOnly cookies | Most secure, automatic management |

## Implementation Checklist

- [ ] Install Tailwind CSS and configure for Next.js
- [ ] Install React Hook Form for form handling
- [ ] Install Better Auth and configure with database
- [ ] Create AuthContext for global auth state
- [ ] Create API client with JWT injection
- [ ] Set up middleware for protected routes
- [ ] Configure TypeScript for strict type checking
- [ ] Set up environment variables (.env.local)

## Security Notes

- JWT tokens stored in httpOnly cookies (not accessible via JavaScript)
- All API requests include Authorization header
- Protected routes check auth state via middleware
- Client-side validation with React Hook Form
- Server-side validation by backend API
- HTTPS required in production
- CORS configured on backend for frontend origin

## Performance Considerations

- Tailwind CSS purging removes unused styles
- React Hook Form uses uncontrolled components (minimal re-renders)
- Component state avoids unnecessary global state updates
- Custom API client has no overhead from large libraries
- Better Auth handles session caching efficiently

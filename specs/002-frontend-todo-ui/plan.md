# Implementation Plan: Frontend UI + API Integration

**Branch**: `002-frontend-todo-ui` | **Date**: 2026-01-23 | **Spec**: [spec.md](./spec.md)
**Status**: Implemented ✅ | **Completed**: 2026-01-23 | **Last Updated**: 2026-01-24
**Input**: Feature specification from `/specs/002-frontend-todo-ui/spec.md`

## Implementation Summary

Successfully implemented a responsive Next.js 16+ frontend with localStorage + cookie-based authentication that integrates with the FastAPI backend. All core features completed including signup/signin, task CRUD operations, responsive design, and proper error handling.

**Key Implementation Details:**
- **Authentication**: localStorage for token storage + cookies for middleware checks
- **Session Management**: 7-day token expiration, automatic redirect on auth failure
- **Styling**: Tailwind CSS v4 with custom color theme defined in globals.css
- **Error Handling**: Comprehensive error boundaries and user-friendly messages
- **Responsive Design**: Mobile-first approach with breakpoints at 320px, 768px, 1024px

## Summary

Implement a responsive Next.js 16+ frontend application with Better Auth authentication that connects to the existing FastAPI backend. The application provides a complete todo management interface with signup/signin flows, task list viewing, task creation, completion toggling, editing, and deletion. All API requests include JWT tokens for authentication, and the UI handles loading, empty, and error states gracefully across mobile and desktop devices.

## Technical Context

**Language/Version**:
- TypeScript 5.0+ with Next.js 16+ (App Router)
- React 18+ (included with Next.js)

**Primary Dependencies**:
- Next.js 16+ (App Router, Server Components, Client Components)
- Better Auth (authentication and session management)
- Tailwind CSS (responsive styling)
- React Hook Form (form validation and handling)

**Storage**: Client-side session storage via Better Auth (JWT tokens)

**Testing**:
- Jest with React Testing Library (component tests)
- Playwright or Cypress (E2E tests - optional)

**Target Platform**:
- Web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Responsive: 320px (mobile) to 1920px+ (desktop)

**Project Type**: Single-page application (SPA) with Next.js App Router

**Performance Goals**:
- Initial page load: <3 seconds
- Task list render: <1 second after data fetch
- UI interactions: <100ms perceived latency
- API requests: <2 seconds average

**Constraints**:
- Must integrate with existing FastAPI backend from SPEC 2
- JWT tokens must be included in all API requests
- Responsive design required (mobile-first approach)
- Better Auth must handle session management
- No complex UI libraries (keep dependencies minimal)

**Scale/Scope**:
- Single-user interface (multi-user via authentication)
- 7 user stories (5 P1, 2 P2)
- 6 main pages/routes (signup, signin, dashboard, task detail, edit, 404)
- Integration with 6 backend API endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Security-First Design ✅ PASS
- **Requirement**: JWT tokens included in all API requests
- **Implementation**: Centralized API client automatically injects Authorization header from Better Auth session
- **Requirement**: Protected routes require authentication
- **Implementation**: Middleware checks authentication state and redirects unauthenticated users to signin
- **Requirement**: Tokens stored securely
- **Implementation**: Better Auth manages token storage using httpOnly cookies or secure storage

### Correctness and Reliability ✅ PASS
- **Requirement**: Consistent error handling across all API calls
- **Implementation**: Centralized API client with standardized error mapping (401→redirect, 403→forbidden, 5xx→error)
- **Requirement**: Loading and error states for all async operations
- **Implementation**: React state management for loading/error/success states in all components

### Clean Architecture ✅ PASS
- **Requirement**: Clear separation of concerns
- **Implementation**:
  - Components: UI presentation layer
  - API Client: Data fetching and authentication layer
  - Better Auth: Authentication and session management layer
  - Types: Shared TypeScript interfaces

### Maintainability ✅ PASS
- **Requirement**: Reusable components and utilities
- **Implementation**:
  - Shared UI components (Button, Input, Card, etc.)
  - Centralized API client for all backend calls
  - Shared TypeScript types for Task and User entities
- **Requirement**: Configuration via environment variables
- **Implementation**: .env.local for API URL and Better Auth settings

### Modern Full-Stack Standards ✅ PASS
- **Requirement**: Next.js App Router conventions
- **Implementation**: app/ directory structure with layouts, pages, and route groups
- **Requirement**: Responsive design
- **Implementation**: Mobile-first Tailwind CSS with responsive breakpoints
- **Requirement**: TypeScript for type safety
- **Implementation**: Strict TypeScript configuration with proper typing

### Test-Driven Development ⚠️ CONDITIONAL
- **Status**: Tests not explicitly required in specification
- **Approach**: Component tests recommended for critical flows (auth, task operations)
- **Recommendation**: Add basic tests for authentication and task CRUD operations

**Gate Status**: ✅ PASS - All mandatory principles satisfied. Testing recommended but not blocking.

## Project Structure

### Documentation (this feature)

```text
specs/002-frontend-todo-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - Technology decisions
├── data-model.md        # Phase 1 output - Frontend data structures
├── quickstart.md        # Phase 1 output - Setup and run instructions
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout with Better Auth provider
│   │   ├── page.tsx             # Landing/redirect page
│   │   ├── signup/
│   │   │   └── page.tsx         # Signup page
│   │   ├── signin/
│   │   │   └── page.tsx         # Signin page
│   │   ├── dashboard/
│   │   │   └── page.tsx         # Task list dashboard
│   │   ├── tasks/
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx     # Task detail view
│   │   │   └── [id]/edit/
│   │   │       └── page.tsx     # Task edit page
│   │   └── middleware.ts        # Auth middleware for protected routes
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SignupForm.tsx
│   │   │   └── SigninForm.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskDetail.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Card.tsx
│   │       ├── Loading.tsx
│   │       └── ErrorMessage.tsx
│   ├── lib/
│   │   ├── auth.ts              # Better Auth configuration
│   │   ├── api-client.ts        # API client with JWT injection
│   │   └── utils.ts             # Utility functions
│   ├── types/
│   │   ├── task.ts              # Task type definitions
│   │   └── user.ts              # User type definitions
│   └── styles/
│       └── globals.css          # Global styles and Tailwind imports
├── public/
│   └── (static assets)
├── .env.local.example           # Environment variable template
├── next.config.js               # Next.js configuration
├── tailwind.config.js           # Tailwind CSS configuration
├── tsconfig.json                # TypeScript configuration
└── package.json                 # Dependencies and scripts
```

**Structure Decision**: Next.js App Router structure selected. Uses app/ directory for routing, components/ for reusable UI, lib/ for utilities, and types/ for TypeScript definitions. This follows Next.js 16+ conventions and enables Server Components where beneficial.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitution principles are satisfied by the proposed architecture.

## Phase 0: Research & Technology Decisions

### Research Tasks

1. **Styling Approach**
   - Research: Tailwind CSS vs CSS Modules vs styled-components for Next.js
   - Research: Mobile-first responsive design patterns
   - Research: Tailwind configuration for custom design system
   - Decision needed: Styling solution selection

2. **State Management**
   - Research: React Context vs Zustand vs component state for auth and tasks
   - Research: Server Components vs Client Components state patterns
   - Research: Optimistic UI updates for task operations
   - Decision needed: State management strategy

3. **Form Handling**
   - Research: React Hook Form vs Formik vs native forms
   - Research: Form validation patterns (client-side and API error handling)
   - Research: Form submission with loading states
   - Decision needed: Form library selection

4. **API Client Implementation**
   - Research: Custom fetch wrapper vs axios vs other HTTP clients
   - Research: JWT token extraction from Better Auth session
   - Research: Error handling and retry strategies
   - Decision needed: API client architecture

5. **Better Auth Configuration**
   - Research: Better Auth setup for Next.js App Router
   - Research: Session management in Server vs Client Components
   - Research: Token storage options (httpOnly cookies vs localStorage)
   - Decision needed: Better Auth integration pattern

### Research Output

See [research.md](./research.md) for detailed findings and decisions.

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Key Frontend Entities**:
- **Task**: id, title, description, completed, created_at, updated_at (mirrors backend)
- **User**: id, email, name (from JWT payload and API)
- **UIState**: loading, error, success states for async operations

**State Management**:
- Authentication state: Better Auth session
- Task list state: Component state or React Context
- Form state: React Hook Form
- UI state: Component state (loading, error)

### Component Architecture

**Page Components** (app/ directory):
- Landing page: Redirects based on auth state
- Signup page: SignupForm component
- Signin page: SigninForm component
- Dashboard page: TaskList component with create form
- Task detail page: TaskDetail component
- Task edit page: TaskForm component (edit mode)

**Reusable Components** (components/ directory):
- Auth components: SignupForm, SigninForm
- Task components: TaskList, TaskCard, TaskForm, TaskDetail
- UI components: Button, Input, Card, Loading, ErrorMessage

**Utilities** (lib/ directory):
- auth.ts: Better Auth configuration
- api-client.ts: Centralized API client with JWT injection
- utils.ts: Helper functions (date formatting, validation, etc.)

### API Integration

**Backend Endpoints** (from SPEC 2):
- POST /api/auth/signup - Create account
- POST /api/auth/signin - Authenticate and get JWT
- GET /api/auth/me - Get current user
- GET /api/{user_id}/tasks - List tasks
- POST /api/{user_id}/tasks - Create task
- GET /api/{user_id}/tasks/{id} - Get task details
- PUT /api/{user_id}/tasks/{id} - Update task
- DELETE /api/{user_id}/tasks/{id} - Delete task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

**API Client Pattern**:
```typescript
// Centralized API client
async function apiClient(endpoint: string, options?: RequestInit) {
  const session = await getSession() // Better Auth
  const token = session?.token

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options?.headers
    }
  })

  if (response.status === 401) {
    // Redirect to signin
    redirect('/signin')
  }

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}
```

### Routing Strategy

**Public Routes**:
- / - Landing page (redirects to dashboard if authenticated, signin if not)
- /signup - User registration
- /signin - User authentication

**Protected Routes** (require authentication):
- /dashboard - Task list and create form
- /tasks/[id] - Task detail view
- /tasks/[id]/edit - Task edit form

**Middleware**: Check authentication state on protected routes and redirect to /signin if not authenticated.

### Quickstart Guide

See [quickstart.md](./quickstart.md) for setup instructions.

## Phase 2: Task Breakdown

**Note**: Task breakdown is generated by `/sp.tasks` command, not `/sp.plan`.

Expected task categories:
1. **Project Setup**: Initialize Next.js, install dependencies, configure TypeScript
2. **Authentication UI**: Signup and signin pages with Better Auth integration
3. **API Client**: Centralized fetch wrapper with JWT injection
4. **Task Components**: TaskList, TaskCard, TaskForm, TaskDetail
5. **Dashboard Page**: Main task list view with create form
6. **Task Detail/Edit Pages**: View and edit individual tasks
7. **Responsive Styling**: Tailwind CSS configuration and mobile-first design
8. **Error Handling**: Loading, empty, and error states
9. **Testing**: Component tests for critical flows (optional)
10. **Documentation**: README with setup and usage instructions

## Architectural Decisions

### Decision 1: Styling Solution

**Options Considered**:
- Tailwind CSS: Utility-first, highly customizable, excellent responsive support
- CSS Modules: Scoped styles, more traditional CSS approach
- styled-components: CSS-in-JS, dynamic styling

**Decision**: Tailwind CSS

**Rationale**:
- Excellent responsive design utilities (mobile-first)
- Fast development with utility classes
- Small bundle size with purging
- Great Next.js integration
- Industry standard for modern React apps

**Trade-offs**:
- Learning curve for utility-first approach
- Can lead to verbose className strings
- Less control over exact CSS output

### Decision 2: State Management

**Options Considered**:
- React Context: Built-in, good for auth state
- Zustand: Lightweight, simple API
- Component state: Simplest, no external dependencies

**Decision**: Component state with React Context for auth

**Rationale**:
- Task list is simple enough for component state
- React Context perfect for auth state (user info, session)
- Avoids unnecessary dependencies
- Easier to understand and maintain

**Trade-offs**:
- May need refactoring if state becomes complex
- Prop drilling for some components
- No built-in devtools

### Decision 3: Form Handling

**Options Considered**:
- React Hook Form: Performant, minimal re-renders
- Formik: Feature-rich, larger bundle
- Native forms: No dependencies, more manual work

**Decision**: React Hook Form

**Rationale**:
- Excellent performance (uncontrolled components)
- Built-in validation support
- Small bundle size
- Great TypeScript support
- Easy integration with API error handling

**Trade-offs**:
- Learning curve for hook-based API
- Less control over form state

### Decision 4: API Client

**Options Considered**:
- Custom fetch wrapper: Full control, minimal dependencies
- axios: Feature-rich, larger bundle
- SWR/React Query: Caching and state management

**Decision**: Custom fetch wrapper

**Rationale**:
- Simple requirements (CRUD operations)
- Full control over error handling
- No additional dependencies
- Easy to integrate with Better Auth
- Sufficient for this use case

**Trade-offs**:
- No built-in caching
- Manual error handling
- No request deduplication

### Decision 5: Better Auth Integration

**Options Considered**:
- httpOnly cookies: Most secure, requires server-side handling
- localStorage: Simple, client-side only
- Better Auth default: Framework-managed

**Decision**: Better Auth default (httpOnly cookies)

**Rationale**:
- Most secure option (XSS protection)
- Better Auth handles complexity
- Works with Server Components
- Industry best practice

**Trade-offs**:
- Requires server-side session handling
- More complex than localStorage
- CORS considerations

## Security Considerations

### Token Security
- JWT tokens stored in httpOnly cookies via Better Auth
- Tokens never exposed in client-side JavaScript
- HTTPS required in production
- Tokens included in Authorization header for API calls

### Authentication Flow
- Protected routes check auth state via middleware
- Unauthenticated users redirected to signin
- Session expiration handled gracefully
- Clear error messages without information leakage

### Input Validation
- Client-side validation with React Hook Form
- Server-side validation by backend API
- XSS prevention via React's built-in escaping
- No direct HTML rendering of user input

### API Security
- All API requests include JWT token
- 401 responses trigger re-authentication
- 403 responses show access denied message
- No sensitive data in URL parameters

## Testing Strategy

### Component Tests (Optional)
- Authentication forms (signup, signin)
- Task CRUD operations
- Loading and error states
- Responsive layout

### Integration Tests (Optional)
- Full authentication flow
- Task creation and completion
- Error handling scenarios

### Manual Testing Checklist
- Signup and signin flows
- Task list display
- Task creation
- Task completion toggle
- Task editing
- Task deletion
- Responsive design (mobile, tablet, desktop)
- Error handling (network failures, API errors)
- Session expiration

## Deployment Considerations

### Environment Variables
- NEXT_PUBLIC_API_URL: Backend API base URL
- BETTER_AUTH_SECRET: Shared secret with backend
- NEXTAUTH_URL: Frontend base URL

### Build Configuration
- Next.js static export or server deployment
- Environment-specific API URLs
- Production optimizations (minification, tree-shaking)

### Production Checklist
- [ ] HTTPS enabled
- [ ] Environment variables configured
- [ ] CORS configured on backend
- [ ] Error logging enabled
- [ ] Performance monitoring
- [ ] Responsive design tested on real devices

## Open Questions

None - all technical decisions resolved through research phase.

## Next Steps

1. Run `/sp.tasks` to generate task breakdown
2. Run `/sp.implement` to execute tasks via specialized agents
3. Use `nextjs-ui-builder` for component implementation
4. Use `secure-auth-agent` for Better Auth integration
5. Test authentication and task operations end-to-end

# Implementation Plan: Authentication + JWT Security

**Branch**: `001-auth-jwt-security` | **Date**: 2026-01-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-auth-jwt-security/spec.md`

## Summary

Implement secure multi-user authentication using Better Auth-issued JWT tokens verified by FastAPI backend. The system enforces strict user isolation by validating JWT signatures on every protected endpoint, extracting authenticated user identity, and ensuring ownership rules prevent cross-user data access. All task API operations require valid JWT tokens with 401 Unauthorized for missing/invalid tokens and 403 Forbidden for ownership violations.

## Technical Context

**Language/Version**:
- Frontend: TypeScript with Next.js 16+ (App Router)
- Backend: Python 3.11+ with FastAPI

**Primary Dependencies**:
- Frontend: Better Auth (authentication library), Next.js, React
- Backend: FastAPI, PyJWT or python-jose (JWT verification), SQLModel (ORM), asyncpg (PostgreSQL driver)

**Storage**: Neon Serverless PostgreSQL with connection pooling (pgbouncer)

**Testing**:
- Frontend: Jest, React Testing Library
- Backend: pytest, pytest-asyncio
- Integration: API contract tests for auth flows

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge) - responsive design
- Backend: Linux server (containerized deployment)

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- JWT token verification: <50ms per request
- Authentication endpoints: 100+ requests/second
- Token issuance: <500ms from credential submission to token delivery

**Constraints**:
- Stateless authentication (no server-side session storage)
- HTTPS required in production for token security
- BETTER_AUTH_SECRET must be cryptographically strong (32+ characters)
- Zero tolerance for cross-user data access

**Scale/Scope**:
- Multi-user system (10k+ users expected)
- All existing task endpoints require authentication retrofit
- 4 new authentication endpoints (signup, signin, logout, me)
- 6 existing task endpoints require JWT verification

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Security-First Design ✅ PASS
- **Requirement**: JWT tokens verified on every protected endpoint using BETTER_AUTH_SECRET
- **Implementation**: FastAPI dependency/middleware validates JWT signature before route execution
- **Requirement**: Authenticated user identity must match {user_id} path parameter
- **Implementation**: Ownership validation in every route handler compares JWT user_id to path parameter
- **Requirement**: Backend queries filter by authenticated user ID
- **Implementation**: All database queries include WHERE user_id = authenticated_user_id clause

### Correctness and Reliability ✅ PASS
- **Requirement**: Consistent JSON responses with appropriate HTTP status codes
- **Implementation**: 401 for auth failures, 403 for ownership violations, standardized error payload format
- **Requirement**: Backend stateless with respect to authentication
- **Implementation**: JWT-based authentication requires no database lookup for token validation

### Clean Architecture ✅ PASS
- **Requirement**: Clear separation between frontend, backend, and database layers
- **Implementation**:
  - Next.js frontend: Better Auth configuration, UI components, API client with token injection
  - FastAPI backend: JWT verification dependency, route handlers, database queries
  - Neon PostgreSQL: User and task data storage with foreign key constraints

### Maintainability ✅ PASS
- **Requirement**: Modular code with reusable components
- **Implementation**:
  - Backend: Centralized auth dependency for reuse across all protected routes
  - Frontend: Centralized API client utility automatically attaches Authorization header
- **Requirement**: Configuration via environment variables
- **Implementation**: BETTER_AUTH_SECRET in .env files (frontend and backend), never hardcoded

### Modern Full-Stack Standards ✅ PASS
- **Requirement**: REST API follows HTTP method semantics
- **Implementation**: POST for signup/signin/logout, GET for user info, existing CRUD endpoints unchanged
- **Requirement**: Responsive frontend
- **Implementation**: Next.js responsive design maintained, auth pages follow same patterns

### Test-Driven Development ⚠️ CONDITIONAL
- **Status**: Tests not explicitly requested in specification
- **Approach**: Security-critical auth flows should be tested even if not mandated
- **Recommendation**: Add integration tests for auth endpoints and ownership enforcement

**Gate Status**: ✅ PASS - All mandatory principles satisfied. TDD recommended but not blocking.

## Project Structure

### Documentation (this feature)

```text
specs/001-auth-jwt-security/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - Better Auth + JWT verification research
├── data-model.md        # Phase 1 output - User entity and JWT payload structure
├── quickstart.md        # Phase 1 output - Setup instructions for auth system
├── contracts/           # Phase 1 output - API contracts for auth endpoints
│   ├── auth-signup.yaml
│   ├── auth-signin.yaml
│   ├── auth-logout.yaml
│   └── auth-me.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py      # JWT verification dependency
│   │   ├── schemas.py           # Auth request/response models
│   │   └── utils.py             # JWT decode/verify utilities
│   ├── routers/
│   │   ├── auth.py              # Auth endpoints (signup, signin, logout, me)
│   │   └── tasks.py             # Existing task routes (add auth dependency)
│   ├── models/
│   │   └── user.py              # User SQLModel (if not exists)
│   └── main.py                  # FastAPI app with CORS config
├── tests/
│   ├── test_auth_endpoints.py  # Auth flow integration tests
│   └── test_ownership.py        # Cross-user access prevention tests
└── .env.example                 # BETTER_AUTH_SECRET template

frontend/
├── src/
│   ├── lib/
│   │   ├── auth.ts              # Better Auth configuration
│   │   └── api-client.ts        # Fetch wrapper with Authorization header
│   ├── app/
│   │   ├── signup/
│   │   │   └── page.tsx         # Signup page
│   │   ├── signin/
│   │   │   └── page.tsx         # Signin page
│   │   └── dashboard/
│   │       └── page.tsx         # Protected dashboard (existing)
│   └── components/
│       └── auth/
│           ├── SignupForm.tsx
│           └── SigninForm.tsx
├── middleware.ts                # Auth middleware for protected routes
└── .env.local.example           # BETTER_AUTH_SECRET template
```

**Structure Decision**: Web application structure selected. Frontend and backend are separate projects with independent deployment. Backend provides REST API, frontend consumes it. Authentication spans both layers: Better Auth in frontend issues tokens, FastAPI in backend verifies them.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitution principles are satisfied by the proposed architecture.

## Phase 0: Research & Technology Decisions

### Research Tasks

1. **Better Auth JWT Configuration**
   - Research: How to configure Better Auth to issue JWT tokens (not just session cookies)
   - Research: JWT payload structure and claims issued by Better Auth
   - Research: Token expiration configuration and refresh token support
   - Decision needed: Better Auth plugin/provider configuration for JWT mode

2. **FastAPI JWT Verification**
   - Research: PyJWT vs python-jose for JWT signature verification
   - Research: Async JWT verification patterns in FastAPI dependencies
   - Research: Error handling for expired/invalid tokens
   - Decision needed: JWT library selection and dependency injection pattern

3. **Shared Secret Management**
   - Research: Best practices for sharing secrets between Next.js and FastAPI
   - Research: Environment variable loading in both frameworks
   - Decision needed: Secret rotation strategy (if needed for production)

4. **Token Transport**
   - Research: Authorization header format and Bearer token standard
   - Research: Frontend token storage (localStorage vs httpOnly cookies vs Better Auth session)
   - Decision needed: Token storage mechanism that works with Better Auth

5. **Error Response Standardization**
   - Research: FastAPI exception handlers for 401/403 responses
   - Research: Frontend error handling for auth failures
   - Decision needed: Error payload format for auth errors

### Research Output

See [research.md](./research.md) for detailed findings and decisions.

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Key Entities**:
- **User**: id (UUID), email (unique), password_hash, name, created_at, updated_at
- **JWT Token Payload**: sub (user_id), email, iat (issued at), exp (expiration)

**Relationships**:
- User → Tasks (one-to-many via user_id foreign key)

**Validation Rules**:
- Email: Valid email format, unique constraint
- Password: Minimum 8 characters, hashed with bcrypt/argon2
- JWT: Signature verified with BETTER_AUTH_SECRET, expiration checked

### API Contracts

See [contracts/](./contracts/) directory for OpenAPI specifications.

**New Endpoints**:
- POST /api/auth/signup - Create user account
- POST /api/auth/signin - Authenticate and issue JWT
- POST /api/auth/logout - Invalidate session (Better Auth)
- GET /api/auth/me - Get current user info

**Modified Endpoints** (add JWT requirement):
- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- GET /api/{user_id}/tasks/{id}
- PUT /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH /api/{user_id}/tasks/{id}/complete

### Quickstart Guide

See [quickstart.md](./quickstart.md) for setup instructions.

## Phase 2: Task Breakdown

**Note**: Task breakdown is generated by `/sp.tasks` command, not `/sp.plan`.

Expected task categories:
1. **Backend Auth Infrastructure**: JWT verification dependency, error handlers
2. **Backend Auth Endpoints**: Signup, signin, logout, me routes
3. **Backend Ownership Enforcement**: Add auth dependency to task routes, validate user_id
4. **Frontend Better Auth Setup**: Install and configure Better Auth with JWT
5. **Frontend API Client**: Build fetch wrapper with Authorization header injection
6. **Frontend Auth Pages**: Signup and signin UI components
7. **Frontend Protected Routes**: Add auth middleware to dashboard and task pages
8. **Integration Testing**: Auth flow tests, ownership violation tests
9. **Documentation**: README updates, environment variable documentation

## Architectural Decisions

### Decision 1: JWT Library Selection (Backend)

**Options Considered**:
- PyJWT: Lightweight, widely used, good documentation
- python-jose: More features (JWE support), heavier dependency
- authlib: Full OAuth/OIDC suite, overkill for JWT-only

**Decision**: PyJWT

**Rationale**:
- Lightweight and focused on JWT only (no unused features)
- Excellent async support for FastAPI
- Better Auth uses standard JWT format, no special features needed
- Simpler dependency tree reduces security surface area

**Trade-offs**:
- No JWE (encrypted JWT) support, but not required for this use case
- If future OAuth integration needed, may need to add python-jose

### Decision 2: Token Storage (Frontend)

**Options Considered**:
- localStorage: Simple, but vulnerable to XSS
- httpOnly cookies: Secure, but requires backend cookie handling
- Better Auth session management: Built-in, framework-integrated

**Decision**: Better Auth session management (default behavior)

**Rationale**:
- Better Auth handles token storage securely by default
- Reduces custom code and potential security mistakes
- Integrates with Better Auth's refresh token mechanism
- Framework handles token injection into requests automatically

**Trade-offs**:
- Less control over token lifecycle
- Must follow Better Auth conventions for token access

### Decision 3: Ownership Validation Strategy

**Options Considered**:
- Middleware: Global validation before route execution
- Dependency: Per-route validation with dependency injection
- Route handler: Manual validation in each handler

**Decision**: FastAPI Dependency with path parameter validation

**Rationale**:
- Explicit and visible in route signatures
- Reusable across all protected routes
- Fails fast before database queries
- Clear error messages for debugging

**Trade-offs**:
- Must remember to add dependency to every protected route
- Slightly more verbose route definitions

### Decision 4: Error Response Format

**Decision**: Standardized JSON error format

```json
{
  "detail": "Human-readable error message",
  "error_code": "UNAUTHORIZED" | "FORBIDDEN" | "INVALID_TOKEN",
  "status_code": 401 | 403
}
```

**Rationale**:
- Consistent error handling across all endpoints
- Machine-readable error codes for frontend logic
- Human-readable messages for debugging
- Follows FastAPI HTTPException pattern

## Security Considerations

### Token Security
- BETTER_AUTH_SECRET must be 32+ characters, cryptographically random
- Tokens transmitted only over HTTPS in production
- Token expiration enforced (default: 7 days, configurable)
- No sensitive data in JWT payload (it's base64-encoded, not encrypted)

### Signature Verification
- Every protected endpoint verifies JWT signature before execution
- No caching of verification results (stateless verification)
- Invalid signatures immediately rejected with 401

### Ownership Enforcement
- Path parameter {user_id} validated against JWT user_id claim
- Mismatch results in 403 Forbidden (not 404 to avoid info leakage)
- Database queries always scoped by authenticated user_id

### Error Handling
- Authentication errors (401) don't leak user existence information
- Authorization errors (403) don't expose other users' data
- Stack traces never exposed in production error responses

## Testing Strategy

### Unit Tests
- JWT verification utility functions
- Token payload extraction and validation
- Error handler responses

### Integration Tests
- Signup flow: valid credentials → account created
- Signin flow: valid credentials → JWT issued
- Protected endpoint: no token → 401
- Protected endpoint: invalid token → 401
- Protected endpoint: expired token → 401
- Ownership violation: user A requests user B's data → 403
- Valid access: user A requests user A's data → 200

### Security Tests
- Cross-user access attempts (all combinations)
- Token tampering (modified signature, modified payload)
- Token replay after logout
- Concurrent requests with same token

## Deployment Considerations

### Environment Variables
- BETTER_AUTH_SECRET: Shared between frontend and backend
- DATABASE_URL: Neon PostgreSQL connection string
- NEXTAUTH_URL: Frontend base URL for Better Auth
- CORS_ORIGINS: Allowed frontend origins for backend

### Production Checklist
- [ ] HTTPS enabled for both frontend and backend
- [ ] BETTER_AUTH_SECRET rotated from development default
- [ ] CORS configured with specific origins (not wildcard)
- [ ] Rate limiting enabled on auth endpoints
- [ ] Database connection pooling configured
- [ ] Error logging enabled (without exposing sensitive data)
- [ ] Token expiration appropriate for use case

## Open Questions

None - all technical decisions resolved through research phase.

## Next Steps

1. Run `/sp.tasks` to generate task breakdown
2. Run `/sp.implement` to execute tasks via specialized agents
3. Use `secure-auth-agent` for auth implementation
4. Use `backend-engineer` for FastAPI route modifications
5. Use `nextjs-ui-builder` for frontend auth pages

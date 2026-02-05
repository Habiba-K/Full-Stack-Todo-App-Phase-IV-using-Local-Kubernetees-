# Research: Authentication + JWT Security

**Feature**: 001-auth-jwt-security
**Date**: 2026-01-22
**Status**: Complete

## Research Task 1: Better Auth JWT Configuration

### Question
How to configure Better Auth to issue JWT tokens (not just session cookies)?

### Findings

**Better Auth Token Mechanism**:
- Better Auth v1.0+ supports JWT tokens by default for API authentication
- Configuration via `auth.ts` file with JWT adapter enabled
- Token payload automatically includes: `sub` (user ID), `email`, `iat`, `exp`
- Default expiration: 7 days (configurable via `jwt.maxAge` option)

**Configuration Pattern**:
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET,
  database: {
    // Database connection for user storage
  },
  jwt: {
    enabled: true,
    maxAge: 60 * 60 * 24 * 7, // 7 days in seconds
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7,
    },
  },
})
```

**Token Access**:
- Better Auth stores JWT in httpOnly cookie by default
- Frontend can access token via `auth.getSession()` for manual API calls
- Token automatically included in requests to Better Auth endpoints

### Decision

**Approach**: Use Better Auth default JWT configuration with httpOnly cookie storage

**Rationale**:
- Secure by default (httpOnly prevents XSS attacks)
- Automatic token refresh handling
- Standard JWT format compatible with FastAPI verification
- No custom token storage logic needed

**Implementation Notes**:
- Frontend API client must extract token from Better Auth session
- Token passed to FastAPI via Authorization header
- BETTER_AUTH_SECRET must be strong (32+ characters, random)

---

## Research Task 2: FastAPI JWT Verification

### Question
PyJWT vs python-jose for JWT signature verification? What's the async pattern?

### Findings

**Library Comparison**:

| Feature | PyJWT | python-jose |
|---------|-------|-------------|
| Size | Lightweight (~50KB) | Heavier (~200KB) |
| JWT Support | Excellent | Excellent |
| JWE Support | No | Yes |
| Async Support | Native | Via sync wrapper |
| Dependencies | Minimal | More dependencies |
| Maintenance | Active | Active |

**Async Verification Pattern**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Annotated

security = HTTPBearer()

async def verify_jwt(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

**Error Handling**:
- `jwt.ExpiredSignatureError`: Token expired → 401
- `jwt.InvalidTokenError`: Invalid signature/format → 401
- `jwt.DecodeError`: Malformed token → 401

### Decision

**Library**: PyJWT

**Rationale**:
- Lightweight with minimal dependencies
- JWT.decode() is CPU-bound (not I/O), so sync is acceptable in async context
- No JWE needed for this use case
- Better performance for simple JWT verification
- Simpler dependency tree = smaller security surface

**Implementation Pattern**: FastAPI dependency injection with HTTPBearer

---

## Research Task 3: Shared Secret Management

### Question
Best practices for sharing BETTER_AUTH_SECRET between Next.js and FastAPI?

### Findings

**Environment Variable Patterns**:

**Next.js**:
- Server-side: `process.env.BETTER_AUTH_SECRET` (no prefix needed)
- Client-side: `process.env.NEXT_PUBLIC_*` (NOT for secrets)
- Loading: Automatic from `.env.local` file

**FastAPI**:
- Pattern: `pydantic-settings` for type-safe config
- Loading: From `.env` file via `python-dotenv`
- Validation: Ensure secret meets minimum requirements

**Secret Requirements**:
- Minimum 32 characters
- Cryptographically random (not human-generated)
- Same value in both environments
- Never committed to version control

**Generation**:
```bash
# Generate secure secret
openssl rand -base64 32
# or
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Decision

**Approach**: Environment variables with validation

**Frontend (.env.local)**:
```
BETTER_AUTH_SECRET=<generated-secret>
NEXTAUTH_URL=http://localhost:3000
```

**Backend (.env)**:
```
BETTER_AUTH_SECRET=<same-generated-secret>
DATABASE_URL=postgresql://...
CORS_ORIGINS=http://localhost:3000
```

**Validation**:
- Backend: Pydantic settings validates secret length on startup
- Frontend: Better Auth validates secret format
- Both: Fail fast if secret missing or invalid

**Production**:
- Use environment variables from deployment platform
- Rotate secret periodically (invalidates existing tokens)
- Never log or expose secret in error messages

---

## Research Task 4: Token Transport

### Question
How should frontend store and transport JWT tokens to FastAPI?

### Findings

**Storage Options**:

| Method | Security | Complexity | Better Auth Compatible |
|--------|----------|------------|------------------------|
| localStorage | Vulnerable to XSS | Low | Manual |
| sessionStorage | Vulnerable to XSS | Low | Manual |
| httpOnly Cookie | XSS-safe | Medium | Yes (default) |
| Better Auth Session | XSS-safe | Low | Yes (native) |

**Better Auth Token Access**:
```typescript
// Get token from Better Auth session
import { auth } from "@/lib/auth"

const session = await auth.api.getSession({
  headers: request.headers,
})

const token = session?.session.token
```

**Transport Pattern**:
```typescript
// API client with automatic token injection
async function apiClient(url: string, options: RequestInit = {}) {
  const session = await auth.api.getSession()

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${session?.session.token}`,
      'Content-Type': 'application/json',
    },
  })
}
```

### Decision

**Storage**: Better Auth session management (httpOnly cookie)

**Transport**: Authorization Bearer header

**Rationale**:
- Better Auth handles secure storage automatically
- httpOnly cookie prevents XSS attacks
- Standard Bearer token format for FastAPI
- Automatic token refresh via Better Auth
- No custom storage logic needed

**Implementation**:
- Frontend: Centralized API client extracts token from Better Auth
- Backend: HTTPBearer dependency reads Authorization header
- Format: `Authorization: Bearer <jwt-token>`

---

## Research Task 5: Error Response Standardization

### Question
How to standardize 401/403 error responses across all endpoints?

### Findings

**FastAPI Exception Handling**:
- Custom exception handlers for consistent responses
- HTTPException with status_code and detail
- Exception handlers registered at app level

**Error Response Format**:
```python
# Standard error response
{
  "detail": "Human-readable message",
  "error_code": "UNAUTHORIZED",
  "status_code": 401
}
```

**Exception Handler Pattern**:
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": get_error_code(exc.status_code),
            "status_code": exc.status_code,
        },
    )
```

**Error Codes**:
- 401: `UNAUTHORIZED` - Missing/invalid/expired token
- 403: `FORBIDDEN` - Valid token, insufficient permissions
- 404: `NOT_FOUND` - Resource doesn't exist (within user scope)
- 422: `VALIDATION_ERROR` - Invalid request payload

### Decision

**Format**: Standardized JSON with error_code field

**Implementation**:
- Custom HTTPException subclasses for auth errors
- Global exception handler for consistent formatting
- Frontend error handling based on error_code

**Error Messages**:
- 401: "Authentication required" / "Token expired" / "Invalid token"
- 403: "Access forbidden" / "Insufficient permissions"
- Avoid leaking information (don't reveal if user exists)

---

## Summary of Decisions

| Research Area | Decision | Key Rationale |
|---------------|----------|---------------|
| Better Auth Config | Default JWT with httpOnly cookie | Secure by default, automatic refresh |
| JWT Library | PyJWT | Lightweight, minimal dependencies |
| Secret Management | Environment variables with validation | Standard practice, fail-fast validation |
| Token Storage | Better Auth session (httpOnly) | XSS-safe, framework-integrated |
| Token Transport | Authorization Bearer header | Standard REST API pattern |
| Error Format | Standardized JSON with error_code | Consistent, machine-readable |

## Implementation Checklist

- [ ] Install PyJWT in backend (`pip install pyjwt`)
- [ ] Install Better Auth in frontend (`npm install better-auth`)
- [ ] Generate BETTER_AUTH_SECRET and add to both .env files
- [ ] Create FastAPI JWT verification dependency
- [ ] Create frontend API client with token injection
- [ ] Implement custom exception handlers for 401/403
- [ ] Add CORS configuration for Authorization header
- [ ] Test token flow end-to-end

## Security Notes

- BETTER_AUTH_SECRET must never be committed to git
- Add `.env` and `.env.local` to `.gitignore`
- Use `.env.example` files with placeholder values
- Validate secret strength on application startup
- Log authentication failures for security monitoring
- Never log token values or secrets

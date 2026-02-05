# Quickstart Guide: Authentication + JWT Security

**Feature**: 001-auth-jwt-security
**Date**: 2026-01-22
**Audience**: Developers setting up the authentication system

## Overview

This guide walks you through setting up JWT-based authentication using Better Auth (frontend) and FastAPI (backend). By the end, you'll have a working multi-user authentication system with secure token verification and ownership enforcement.

## Prerequisites

**Frontend**:
- Node.js 18+ and npm/yarn/pnpm
- Next.js 16+ project initialized
- TypeScript configured

**Backend**:
- Python 3.11+
- FastAPI project initialized
- Neon PostgreSQL database provisioned

**Tools**:
- Git for version control
- Code editor (VS Code recommended)
- API testing tool (Postman, Thunder Client, or curl)

## Setup Steps

### Step 1: Generate Shared Secret

Generate a cryptographically secure secret for JWT signing:

```bash
# Option 1: Using OpenSSL
openssl rand -base64 32

# Option 2: Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Option 3: Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

**Important**: Save this secret - you'll need it for both frontend and backend.

---

### Step 2: Backend Setup (FastAPI)

#### 2.1 Install Dependencies

```bash
cd backend
pip install fastapi uvicorn pyjwt python-dotenv sqlmodel asyncpg psycopg2-binary bcrypt
```

**Dependencies**:
- `pyjwt`: JWT token verification
- `bcrypt`: Password hashing
- `sqlmodel`: ORM for database operations
- `asyncpg`: Async PostgreSQL driver
- `python-dotenv`: Environment variable loading

#### 2.2 Configure Environment Variables

Create `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@host/database

# Authentication
BETTER_AUTH_SECRET=<your-generated-secret-from-step-1>

# CORS
CORS_ORIGINS=http://localhost:3000

# Server
HOST=0.0.0.0
PORT=8000
```

Create `backend/.env.example` (commit this to git):

```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-here-minimum-32-characters
CORS_ORIGINS=http://localhost:3000
HOST=0.0.0.0
PORT=8000
```

#### 2.3 Create Database Tables

Run migration to create users table:

```sql
-- Run this in your Neon PostgreSQL console or via migration tool
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

#### 2.4 Create Auth Dependency

Create `backend/src/auth/dependencies.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Annotated
import os

security = HTTPBearer()

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

async def verify_jwt(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            BETTER_AUTH_SECRET,
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

#### 2.5 Start Backend Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Verify server is running: http://localhost:8000/docs

---

### Step 3: Frontend Setup (Next.js)

#### 3.1 Install Dependencies

```bash
cd frontend
npm install better-auth
# or
yarn add better-auth
# or
pnpm add better-auth
```

#### 3.2 Configure Environment Variables

Create `frontend/.env.local`:

```env
# Authentication
BETTER_AUTH_SECRET=<same-secret-from-step-1>
NEXTAUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Create `frontend/.env.local.example` (commit this to git):

```env
BETTER_AUTH_SECRET=your-secret-here-minimum-32-characters
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 3.3 Configure Better Auth

Create `frontend/src/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  database: {
    // Configure database connection for Better Auth
    // This connects to the same database as backend
  },
  jwt: {
    enabled: true,
    maxAge: 60 * 60 * 24 * 7, // 7 days
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7,
    },
  },
})
```

#### 3.4 Create API Client

Create `frontend/src/lib/api-client.ts`:

```typescript
import { auth } from "./auth"

export async function apiClient(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const session = await auth.api.getSession()

  return fetch(`${process.env.NEXT_PUBLIC_API_URL}${url}`, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${session?.session.token}`,
      'Content-Type': 'application/json',
    },
  })
}
```

#### 3.5 Start Frontend Server

```bash
cd frontend
npm run dev
# or
yarn dev
# or
pnpm dev
```

Verify frontend is running: http://localhost:3000

---

### Step 4: Verify Authentication Flow

#### 4.1 Test Signup

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }'
```

Expected response (201):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "test@example.com",
  "name": "Test User",
  "created_at": "2026-01-22T10:30:00Z"
}
```

#### 4.2 Test Signin

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

Expected response (200):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "name": "Test User"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-01-29T10:30:00Z"
}
```

Save the token for next steps.

#### 4.3 Test Protected Endpoint

```bash
# Replace <TOKEN> with the token from signin response
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```

Expected response (200):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "test@example.com",
  "name": "Test User",
  "created_at": "2026-01-22T10:30:00Z",
  "updated_at": "2026-01-22T10:30:00Z"
}
```

#### 4.4 Test Ownership Enforcement

```bash
# Try to access another user's tasks (should fail with 403)
curl -X GET http://localhost:8000/api/<different-user-id>/tasks \
  -H "Authorization: Bearer <TOKEN>"
```

Expected response (403):
```json
{
  "detail": "Access forbidden",
  "error_code": "FORBIDDEN",
  "status_code": 403
}
```

---

## Common Issues and Solutions

### Issue 1: "Invalid token" error

**Symptoms**: All protected endpoints return 401 with "Invalid token"

**Causes**:
- BETTER_AUTH_SECRET mismatch between frontend and backend
- Token format incorrect (missing "Bearer " prefix)
- Token expired

**Solutions**:
1. Verify both `.env` files have identical BETTER_AUTH_SECRET
2. Check Authorization header format: `Bearer <token>`
3. Generate new token by signing in again

### Issue 2: CORS errors in browser

**Symptoms**: Browser console shows CORS policy errors

**Causes**:
- Backend CORS_ORIGINS doesn't include frontend URL
- Authorization header not allowed in CORS config

**Solutions**:
1. Add frontend URL to backend CORS_ORIGINS
2. Ensure FastAPI CORS middleware allows Authorization header:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 3: Database connection errors

**Symptoms**: Backend crashes with "connection refused" or "authentication failed"

**Causes**:
- Incorrect DATABASE_URL
- Neon database not accessible
- Connection pooling not configured

**Solutions**:
1. Verify DATABASE_URL format: `postgresql://user:password@host/database`
2. Check Neon dashboard for connection string
3. Enable connection pooling in Neon settings

### Issue 4: Password hashing errors

**Symptoms**: Signup fails with "Internal server error"

**Causes**:
- bcrypt not installed
- Password hashing function not implemented

**Solutions**:
1. Install bcrypt: `pip install bcrypt`
2. Implement password hashing in signup endpoint

---

## Security Checklist

Before deploying to production:

- [ ] BETTER_AUTH_SECRET is 32+ characters and cryptographically random
- [ ] BETTER_AUTH_SECRET is different from development secret
- [ ] `.env` and `.env.local` files are in `.gitignore`
- [ ] HTTPS enabled for both frontend and backend
- [ ] CORS_ORIGINS set to specific domains (not wildcard)
- [ ] Database connection uses SSL/TLS
- [ ] Rate limiting enabled on auth endpoints
- [ ] Error messages don't leak sensitive information
- [ ] Passwords hashed with bcrypt (cost 12) or argon2id
- [ ] Token expiration appropriate for use case (7 days default)

---

## Next Steps

1. **Implement Auth Pages**: Create signup and signin UI in Next.js
2. **Add Protected Routes**: Use middleware to protect dashboard pages
3. **Implement Logout**: Add logout button and session invalidation
4. **Add Error Handling**: Display user-friendly error messages
5. **Write Tests**: Add integration tests for auth flows
6. **Deploy**: Deploy frontend and backend to production

---

## Additional Resources

**Better Auth Documentation**: https://better-auth.com/docs
**FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/
**PyJWT Documentation**: https://pyjwt.readthedocs.io/
**Neon PostgreSQL**: https://neon.tech/docs

---

## Support

If you encounter issues not covered in this guide:

1. Check the [research.md](./research.md) for detailed technical decisions
2. Review [data-model.md](./data-model.md) for database schema
3. Consult [contracts/](./contracts/) for API specifications
4. Review [plan.md](./plan.md) for architectural decisions

For bugs or feature requests, create an issue in the project repository.

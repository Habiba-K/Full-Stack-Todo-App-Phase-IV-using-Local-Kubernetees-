# Data Model: Authentication + JWT Security

**Feature**: 001-auth-jwt-security
**Date**: 2026-01-22
**Status**: Complete

## Overview

This document defines the data entities and structures for the authentication system. The model supports multi-user authentication with JWT tokens, user account management, and secure data isolation.

## Entities

### User Entity

**Purpose**: Represents a registered user account in the system.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique user identifier |
| email | String | Unique, Not Null, Max 255 chars | User's email address (login identifier) |
| password_hash | String | Not Null, Max 255 chars | Bcrypt/Argon2 hashed password |
| name | String | Nullable, Max 100 chars | User's display name (optional) |
| created_at | Timestamp | Not Null, Default NOW() | Account creation timestamp |
| updated_at | Timestamp | Not Null, Default NOW() | Last update timestamp |

**Validation Rules**:
- Email must be valid email format (RFC 5322)
- Email must be unique (case-insensitive)
- Password must be hashed before storage (never store plain text)
- Password hash uses bcrypt with cost factor 12 or argon2id
- Name is optional but if provided, must be 1-100 characters

**Indexes**:
- Primary index on `id` (UUID)
- Unique index on `email` (for login lookups)
- Index on `created_at` (for user analytics)

**Database Schema (PostgreSQL)**:
```sql
CREATE TABLE users (
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

**SQLModel Definition (Backend)**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    name: str | None = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### JWT Token Payload

**Purpose**: Contains claims embedded in JWT tokens issued by Better Auth and verified by FastAPI.

**Structure**:

| Claim | Type | Required | Description |
|-------|------|----------|-------------|
| sub | String (UUID) | Yes | Subject - User ID |
| email | String | Yes | User's email address |
| iat | Integer (Unix timestamp) | Yes | Issued At - Token creation time |
| exp | Integer (Unix timestamp) | Yes | Expiration - Token expiry time |
| jti | String (UUID) | Optional | JWT ID - Unique token identifier |

**Example Payload**:
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "iat": 1706000000,
  "exp": 1706604800,
  "jti": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Validation Rules**:
- `sub` must be valid UUID matching existing user ID
- `email` must match user's current email in database
- `exp` must be in the future (token not expired)
- `iat` must be in the past (token not issued in future)
- Token signature must be valid (verified with BETTER_AUTH_SECRET)

**Token Lifecycle**:
1. **Issuance**: Better Auth creates token on successful signin
2. **Storage**: Frontend stores in httpOnly cookie via Better Auth
3. **Transport**: Frontend includes in Authorization header for API calls
4. **Verification**: FastAPI verifies signature and expiration on each request
5. **Expiration**: Token expires after 7 days (configurable)
6. **Refresh**: Better Auth handles automatic refresh (if configured)

**Security Notes**:
- Token is signed, not encrypted (payload is base64-encoded)
- Never include sensitive data in payload (passwords, payment info)
- Token signature prevents tampering
- Expiration enforces time-limited access

---

## Relationships

### User → Tasks (One-to-Many)

**Description**: Each user owns zero or more tasks. Tasks are isolated by user_id.

**Foreign Key**: `tasks.user_id` references `users.id`

**Constraints**:
- ON DELETE CASCADE: Deleting user deletes all their tasks
- NOT NULL: Every task must belong to a user

**Query Pattern**:
```sql
-- Get all tasks for authenticated user
SELECT * FROM tasks WHERE user_id = :authenticated_user_id;

-- Ownership validation
SELECT id FROM tasks
WHERE id = :task_id AND user_id = :authenticated_user_id;
```

**Enforcement**:
- Backend MUST filter all task queries by authenticated user_id
- Path parameter {user_id} MUST match JWT user_id claim
- Cross-user access attempts return 403 Forbidden

---

## State Transitions

### User Account States

```
[No Account]
    ↓ (signup with valid credentials)
[Active Account]
    ↓ (signin with correct password)
[Authenticated Session]
    ↓ (logout or token expiration)
[Active Account]
```

**State Descriptions**:
- **No Account**: User has not registered
- **Active Account**: User registered but not currently authenticated
- **Authenticated Session**: User has valid JWT token

**Transitions**:
- Signup: Creates user record with hashed password
- Signin: Issues JWT token with user claims
- Logout: Invalidates session (Better Auth handles)
- Token Expiration: Automatic after 7 days (or configured duration)

---

## Validation Rules Summary

### User Registration
- Email: Valid format, unique, max 255 characters
- Password: Minimum 8 characters (enforced by Better Auth)
- Name: Optional, max 100 characters if provided

### User Authentication
- Email: Must exist in database
- Password: Must match stored hash
- Account: Must be active (not deleted/suspended)

### JWT Token
- Signature: Must be valid (BETTER_AUTH_SECRET)
- Expiration: Must be in future
- User ID: Must exist in database
- Format: Standard JWT with HS256 algorithm

### Ownership Validation
- Path {user_id}: Must match JWT sub claim
- Database queries: Must filter by authenticated user_id
- Cross-user access: Always rejected with 403

---

## Data Access Patterns

### Authentication Flow
1. User submits credentials to Better Auth
2. Better Auth validates against users table
3. Better Auth issues JWT with user claims
4. Frontend stores token in httpOnly cookie
5. Frontend includes token in API requests

### Protected Resource Access
1. Frontend sends request with Authorization header
2. FastAPI extracts and verifies JWT signature
3. FastAPI extracts user_id from JWT payload
4. FastAPI validates {user_id} path param matches JWT user_id
5. FastAPI queries database filtered by user_id
6. FastAPI returns user's data only

### Ownership Enforcement
```python
# Pseudo-code for ownership validation
async def validate_ownership(
    user_id_from_path: UUID,
    jwt_payload: dict
) -> None:
    authenticated_user_id = UUID(jwt_payload["sub"])

    if user_id_from_path != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden"
        )
```

---

## Migration Strategy

### New Tables
- `users` table (if not exists)

### Modified Tables
- `tasks` table: Ensure `user_id` foreign key exists

### Migration Steps
1. Create users table with indexes
2. Add user_id foreign key to tasks table (if missing)
3. Ensure existing tasks have valid user_id values
4. Add indexes for performance (email, created_at)

### Rollback Strategy
- Drop users table
- Remove user_id foreign key from tasks
- Restore previous authentication mechanism

---

## Performance Considerations

### Indexes
- `users.email`: Fast login lookups (unique index)
- `users.id`: Primary key lookups for JWT validation
- `tasks.user_id`: Fast filtering for user's tasks

### Query Optimization
- Use prepared statements for all queries
- Index foreign keys for JOIN performance
- Avoid N+1 queries (fetch user with tasks in single query if needed)

### Caching
- JWT verification is stateless (no database lookup needed)
- User data can be cached after JWT verification (optional)
- Cache invalidation on user updates

---

## Security Considerations

### Password Storage
- Never store plain text passwords
- Use bcrypt (cost 12) or argon2id for hashing
- Salt is automatically included in hash

### Token Security
- JWT signature prevents tampering
- Expiration limits token lifetime
- HTTPS required to prevent token interception

### Data Isolation
- All queries filtered by authenticated user_id
- Foreign key constraints enforce referential integrity
- Database-level isolation via WHERE clauses

### Audit Trail
- created_at and updated_at timestamps on all entities
- Consider adding authentication_logs table for security monitoring (future enhancement)

---

## Future Enhancements

**Not in current scope, but documented for future reference**:

1. **Email Verification**: Add `email_verified` boolean and verification token
2. **Password Reset**: Add reset token and expiration fields
3. **Account Status**: Add `status` enum (active, suspended, deleted)
4. **Two-Factor Authentication**: Add 2FA secret and backup codes
5. **Session Management**: Add sessions table for token revocation
6. **Audit Logging**: Add authentication_logs table for security events
7. **User Roles**: Add roles and permissions for RBAC

These enhancements are explicitly out of scope for the current specification but may be added in future iterations.

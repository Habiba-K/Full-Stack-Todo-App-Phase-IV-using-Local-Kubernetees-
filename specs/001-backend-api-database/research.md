# Research: Backend REST API + Database

**Feature**: Backend REST API + Database
**Date**: 2026-01-22
**Status**: Complete

## Overview

This document captures research findings and technical decisions for implementing a FastAPI-based REST API with SQLModel ORM and Neon Serverless PostgreSQL storage. The focus is on best practices for CRUD operations, user ownership enforcement, and preparing for future JWT authentication integration.

## Key Technical Decisions

### 1. FastAPI Framework Selection

**Decision**: Use FastAPI as the web framework

**Rationale**:
- Native async/await support for high concurrency
- Automatic OpenAPI/Swagger documentation generation (meets SC-010)
- Built-in Pydantic validation for request/response (meets FR-011)
- Type hints provide IDE support and reduce errors
- Excellent performance (comparable to Node.js and Go)
- Large ecosystem and active community

**Alternatives Considered**:
- **Flask**: Simpler but lacks async support and automatic validation
- **Django REST Framework**: More opinionated, heavier, includes ORM we don't need (using SQLModel)
- **Rejected because**: FastAPI provides better performance, automatic docs, and native async support needed for database operations

### 2. SQLModel ORM Selection

**Decision**: Use SQLModel for database operations

**Rationale**:
- Combines SQLAlchemy (mature ORM) with Pydantic (validation)
- Type hints for database models match API schemas
- Reduces code duplication between DB models and API schemas
- Built-in support for async operations
- Excellent integration with FastAPI
- Simpler than raw SQLAlchemy for straightforward CRUD operations

**Alternatives Considered**:
- **Raw SQLAlchemy**: More powerful but more verbose, steeper learning curve
- **Tortoise ORM**: Async-first but smaller ecosystem
- **Rejected because**: SQLModel provides the best balance of simplicity and power for this use case

### 3. Neon Serverless PostgreSQL Connection Strategy

**Decision**: Use connection pooling with pgbouncer (Neon's built-in pooler)

**Rationale**:
- Neon Serverless has connection limits (important for serverless/lambda deployments)
- Pgbouncer pooling mode reduces connection overhead
- FastAPI async operations work well with pooled connections
- Neon provides connection pooling URL format: `postgresql://user:pass@host/db?sslmode=require&pgbouncer=true`
- Prevents "too many connections" errors under load

**Implementation Details**:
- Use Neon's pooled connection string in DATABASE_URL
- Configure SQLModel engine with appropriate pool settings
- Use async session management with dependency injection

**Alternatives Considered**:
- **Direct connections**: Simpler but hits connection limits quickly
- **External pooler (PgBouncer separately)**: More complex deployment
- **Rejected because**: Neon's built-in pooling is optimized for their serverless architecture

### 4. User Ownership Enforcement Pattern

**Decision**: Enforce user ownership at the service layer with user_id from URL path

**Rationale**:
- All queries filter by user_id from path parameter: `/api/{user_id}/tasks`
- Service layer adds `WHERE user_id = {user_id}` to all queries
- Prevents accidental data leakage between users
- Prepares for SPEC 2 where JWT will validate user_id matches authenticated user
- Clear separation: router extracts user_id, service enforces filtering

**Implementation Pattern**:
```python
# Router extracts user_id from path
@router.get("/api/{user_id}/tasks")
async def list_tasks(user_id: str, db: Session = Depends(get_db)):
    return task_service.get_user_tasks(db, user_id)

# Service enforces filtering
def get_user_tasks(db: Session, user_id: str):
    return db.query(Task).filter(Task.user_id == user_id).all()
```

**Alternatives Considered**:
- **Database-level row security**: More secure but complex setup
- **Middleware-based filtering**: Less explicit, harder to audit
- **Rejected because**: Service-layer filtering is explicit, testable, and prepares for JWT integration

### 5. Database Schema Design

**Decision**: Single `tasks` table with user_id as indexed foreign key reference

**Rationale**:
- Simple schema matches requirements (no complex relationships)
- user_id as string/UUID allows flexibility (users table in SPEC 2)
- Index on user_id ensures fast queries (meets SC-009: <100ms)
- Timestamps (created_at, updated_at) for audit trail (FR-013)
- completed boolean for status tracking (FR-007)

**Schema**:
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

**Alternatives Considered**:
- **Soft deletes (deleted_at column)**: Adds complexity, not required in spec
- **Separate status enum table**: Over-engineering for boolean flag
- **Rejected because**: Simple schema meets all requirements without unnecessary complexity

### 6. Error Handling Strategy

**Decision**: Use FastAPI exception handlers with custom exceptions

**Rationale**:
- Consistent error responses across all endpoints (meets FR-009, FR-010)
- Custom exceptions for domain errors (TaskNotFound, ValidationError)
- FastAPI automatically converts to proper HTTP status codes
- Clear error messages for debugging (meets SC-006)

**HTTP Status Code Mapping**:
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content or 200 OK: Successful DELETE
- 404 Not Found: Task doesn't exist or doesn't belong to user
- 422 Unprocessable Entity: Validation errors (automatic via Pydantic)
- 500 Internal Server Error: Unexpected errors (with logging)

**Alternatives Considered**:
- **Manual status code returns**: Error-prone, inconsistent
- **Generic error responses**: Less informative for debugging
- **Rejected because**: FastAPI's exception handling provides consistency and clarity

### 7. Request/Response Schema Design

**Decision**: Separate Pydantic schemas for create, update, and response

**Rationale**:
- **TaskCreate**: Only fields needed for creation (title, description optional)
- **TaskUpdate**: All fields optional (partial updates)
- **TaskResponse**: All fields including id, timestamps (read-only)
- Prevents clients from setting id, timestamps, or user_id directly
- Clear API contract (meets FR-010)

**Schema Structure**:
```python
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: UUID
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

**Alternatives Considered**:
- **Single schema for all operations**: Confusing, allows invalid operations
- **No schemas (dict responses)**: No validation, no documentation
- **Rejected because**: Separate schemas provide clear contracts and validation

### 8. Async vs Sync Database Operations

**Decision**: Use async database operations with SQLModel

**Rationale**:
- FastAPI is async-first framework
- Async operations allow handling multiple requests concurrently (meets SC-005: 100 concurrent requests)
- Better resource utilization under load
- Neon PostgreSQL supports async connections
- Minimal code difference from sync (just add `async`/`await`)

**Implementation**:
- Use `AsyncSession` from SQLModel
- Async database dependency: `async def get_db()`
- All route handlers and service methods are async

**Alternatives Considered**:
- **Sync operations**: Simpler but blocks threads, lower concurrency
- **Rejected because**: Async provides better performance for I/O-bound operations

### 9. Environment Configuration

**Decision**: Use python-dotenv for environment variable management

**Rationale**:
- Simple, standard approach for Python applications
- Supports .env files for local development
- Production uses actual environment variables
- Single source of truth for configuration (DATABASE_URL)
- No hardcoded secrets (meets constitution principle IV)

**Configuration Structure**:
```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

**Alternatives Considered**:
- **Hardcoded config**: Insecure, inflexible
- **Config files (YAML/JSON)**: More complex, secrets in version control
- **Rejected because**: Environment variables are standard for 12-factor apps

### 10. API Endpoint Structure

**Decision**: RESTful endpoints under `/api/{user_id}/tasks` prefix

**Rationale**:
- Clear resource hierarchy: user → tasks
- Follows REST conventions (meets constitution principle V)
- user_id in path makes ownership explicit
- Prepares for SPEC 2 where JWT will validate user_id
- Standard HTTP methods for operations

**Endpoint Design**:
- `GET /api/{user_id}/tasks` - List all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get single task
- `PUT /api/{user_id}/tasks/{id}` - Update task (full)
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

**Alternatives Considered**:
- **Flat structure `/api/tasks?user_id=X`**: Less RESTful, user_id in query string
- **No user_id in path**: Requires JWT immediately, not suitable for SPEC 1
- **Rejected because**: Path-based user_id is explicit and prepares for authentication

## Best Practices Applied

### FastAPI Best Practices
1. **Dependency Injection**: Use `Depends()` for database sessions
2. **Router Organization**: Separate routers for different resources
3. **Automatic Documentation**: OpenAPI/Swagger generated automatically
4. **Type Hints**: Full type coverage for IDE support and validation
5. **Async Operations**: Leverage async/await for I/O operations

### SQLModel Best Practices
1. **Model Definition**: Use SQLModel for both ORM and Pydantic validation
2. **Session Management**: Use context managers for session lifecycle
3. **Query Optimization**: Add indexes on frequently queried columns
4. **Timestamps**: Automatic created_at/updated_at tracking

### Neon PostgreSQL Best Practices
1. **Connection Pooling**: Use Neon's built-in pgbouncer pooling
2. **SSL Connections**: Always use sslmode=require
3. **Async Connections**: Use asyncpg driver for async operations
4. **Index Strategy**: Index user_id for fast user-scoped queries

### Security Best Practices (Pre-Auth)
1. **User Scoping**: All queries filter by user_id from path
2. **Input Validation**: Pydantic schemas validate all inputs
3. **No SQL Injection**: SQLModel uses parameterized queries
4. **Environment Variables**: No secrets in code
5. **Prepared for JWT**: Architecture ready for SPEC 2 authentication

## Performance Considerations

### Database Query Optimization
- Index on `user_id` column for fast filtering
- Limit result sets (consider pagination in future)
- Use async operations to avoid blocking
- Connection pooling to reduce overhead

### API Response Time
- Target: <2 seconds for typical operations (SC-002)
- Async operations allow concurrent request handling
- Database queries optimized with indexes (<100ms target)
- Minimal business logic in service layer

### Concurrency
- Target: 100 concurrent requests (SC-005)
- Async FastAPI + async database operations
- Connection pooling prevents connection exhaustion
- Stateless design allows horizontal scaling

## Risks and Mitigations

### Risk 1: Connection Pool Exhaustion
**Mitigation**: Use Neon's pgbouncer pooling, configure appropriate pool size

### Risk 2: User ID Spoofing (Pre-Auth)
**Mitigation**: Document that SPEC 2 will add JWT validation, current implementation is for testing only

### Risk 3: Database Migration Management
**Mitigation**: Use Alembic for migrations (to be added in implementation phase)

### Risk 4: Large Result Sets
**Mitigation**: Document pagination as future enhancement, current spec returns all tasks

## Next Steps (Phase 1)

1. Create detailed data model specification (data-model.md)
2. Generate OpenAPI contract (contracts/openapi.yaml)
3. Create quickstart guide (quickstart.md)
4. Update agent context with technology decisions

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Neon PostgreSQL Documentation: https://neon.tech/docs/
- Pydantic Documentation: https://docs.pydantic.dev/
- REST API Best Practices: https://restfulapi.net/

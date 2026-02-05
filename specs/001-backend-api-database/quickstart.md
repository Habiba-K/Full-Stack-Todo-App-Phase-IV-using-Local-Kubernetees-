# Quickstart Guide: Backend REST API + Database

**Feature**: Backend REST API + Database
**Date**: 2026-01-22
**Audience**: Developers implementing or testing the API

## Overview

This guide provides step-by-step instructions to set up, run, and test the Task Management REST API with Neon Serverless PostgreSQL.

## Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL account (free tier available at https://neon.tech)
- Git (for cloning the repository)
- curl or Postman (for API testing)

## Setup Instructions

### 1. Get Neon PostgreSQL Connection String

1. Sign up for Neon at https://neon.tech
2. Create a new project
3. Copy the connection string (looks like: `postgresql://user:password@host/database?sslmode=require`)
4. Note: Use the **pooled connection string** for better performance (includes `?pgbouncer=true`)

### 2. Clone and Navigate to Project

```bash
cd backend
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt** should contain:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

### 5. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# .env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require&pgbouncer=true
```

Replace with your actual Neon connection string.

### 6. Initialize Database

The database tables will be created automatically on first run using SQLModel's `create_all()` method.

Alternatively, use Alembic for migrations (recommended for production):

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Create tasks table"

# Apply migration
alembic upgrade head
```

### 7. Run the API Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

### 8. Verify Installation

Open your browser and navigate to:
- API Documentation: http://localhost:8000/docs (Swagger UI)
- Alternative Docs: http://localhost:8000/redoc (ReDoc)

## API Usage Examples

### Example 1: Create a Task

```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation"
  }'
```

**Expected Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "completed": false,
  "created_at": "2026-01-22T10:00:00Z",
  "updated_at": "2026-01-22T10:00:00Z"
}
```

### Example 2: List All Tasks for a User

```bash
curl -X GET "http://localhost:8000/api/user123/tasks"
```

**Expected Response (200 OK)**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123",
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "completed": false,
    "created_at": "2026-01-22T10:00:00Z",
    "updated_at": "2026-01-22T10:00:00Z"
  }
]
```

### Example 3: Get a Specific Task

```bash
curl -X GET "http://localhost:8000/api/user123/tasks/550e8400-e29b-41d4-a716-446655440000"
```

**Expected Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "completed": false,
  "created_at": "2026-01-22T10:00:00Z",
  "updated_at": "2026-01-22T10:00:00Z"
}
```

### Example 4: Update a Task

```bash
curl -X PUT "http://localhost:8000/api/user123/tasks/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation (updated)",
    "description": "Write comprehensive API documentation with examples",
    "completed": false
  }'
```

**Expected Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "title": "Complete project documentation (updated)",
  "description": "Write comprehensive API documentation with examples",
  "completed": false,
  "created_at": "2026-01-22T10:00:00Z",
  "updated_at": "2026-01-22T12:00:00Z"
}
```

### Example 5: Toggle Task Completion

```bash
curl -X PATCH "http://localhost:8000/api/user123/tasks/550e8400-e29b-41d4-a716-446655440000/complete"
```

**Expected Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "title": "Complete project documentation (updated)",
  "description": "Write comprehensive API documentation with examples",
  "completed": true,
  "created_at": "2026-01-22T10:00:00Z",
  "updated_at": "2026-01-22T13:00:00Z"
}
```

### Example 6: Delete a Task

```bash
curl -X DELETE "http://localhost:8000/api/user123/tasks/550e8400-e29b-41d4-a716-446655440000"
```

**Expected Response (200 OK)**:
```json
{
  "message": "Task deleted successfully"
}
```

## Testing User Ownership Enforcement

### Test 1: User A Cannot Access User B's Tasks

```bash
# Create task for user A
curl -X POST "http://localhost:8000/api/userA/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "User A task"}'

# Try to access with user B (should return empty list)
curl -X GET "http://localhost:8000/api/userB/tasks"
```

**Expected**: User B sees empty list, not User A's task.

### Test 2: User B Cannot Access User A's Task by ID

```bash
# Get task ID from User A's task creation response
TASK_ID="550e8400-e29b-41d4-a716-446655440000"

# Try to access as User B (should return 404)
curl -X GET "http://localhost:8000/api/userB/tasks/$TASK_ID"
```

**Expected Response (404 Not Found)**:
```json
{
  "detail": "Task not found"
}
```

## Error Handling Examples

### Validation Error: Missing Title

```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Task without title"
  }'
```

**Expected Response (422 Validation Error)**:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Validation Error: Title Too Long

```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "'$(python -c "print('a' * 501)")'"
  }'
```

**Expected Response (422 Validation Error)**:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 500 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

### Not Found Error: Task Doesn't Exist

```bash
curl -X GET "http://localhost:8000/api/user123/tasks/00000000-0000-0000-0000-000000000000"
```

**Expected Response (404 Not Found)**:
```json
{
  "detail": "Task not found"
}
```

## Verification Checklist

Use this checklist to verify the implementation meets all requirements:

### Persistence Verification
- [ ] Create a task, restart the server, verify task still exists
- [ ] Tasks survive application restarts (stored in Neon PostgreSQL)

### User Ownership Verification
- [ ] User A can list only their own tasks
- [ ] User A cannot access User B's tasks by changing user_id in URL
- [ ] User A cannot update/delete User B's tasks
- [ ] Attempting to access another user's task returns 404

### CRUD Operations Verification
- [ ] Create task with title only (description optional)
- [ ] Create task with title and description
- [ ] List all tasks for a user (returns array)
- [ ] Get single task by ID
- [ ] Update task title and description
- [ ] Toggle task completion status (false → true → false)
- [ ] Delete task permanently

### Validation Verification
- [ ] Creating task without title returns 422 error
- [ ] Creating task with empty title returns 422 error
- [ ] Creating task with title > 500 chars returns 422 error
- [ ] Creating task with description > 5000 chars returns 422 error

### HTTP Status Codes Verification
- [ ] POST /tasks returns 201 Created
- [ ] GET /tasks returns 200 OK
- [ ] GET /tasks/{id} returns 200 OK (found) or 404 Not Found
- [ ] PUT /tasks/{id} returns 200 OK (updated) or 404 Not Found
- [ ] PATCH /tasks/{id}/complete returns 200 OK or 404 Not Found
- [ ] DELETE /tasks/{id} returns 200 OK or 404 Not Found
- [ ] Invalid payloads return 422 Validation Error

### Performance Verification
- [ ] List tasks for user with 100 tasks completes in < 2 seconds
- [ ] Single task operations complete in < 2 seconds
- [ ] Database queries complete in < 100ms (check logs)

## Troubleshooting

### Issue: "Connection refused" error

**Solution**: Verify Neon connection string is correct and database is accessible.

```bash
# Test connection with psql
psql "postgresql://user:password@host/database?sslmode=require"
```

### Issue: "Too many connections" error

**Solution**: Use Neon's pooled connection string with `?pgbouncer=true`.

### Issue: "Table does not exist" error

**Solution**: Run database migrations or ensure `create_all()` is called on startup.

```python
# In src/main.py
from src.database import engine
from src.models.task import Task

@app.on_event("startup")
async def startup():
    SQLModel.metadata.create_all(engine)
```

### Issue: Tasks not persisting after restart

**Solution**: Verify DATABASE_URL is set correctly and not using in-memory database.

### Issue: Validation errors not showing

**Solution**: Ensure Pydantic models are used in route definitions with proper type hints.

## Next Steps

After verifying the API works correctly:

1. **Add Tests**: Write unit and integration tests (optional for SPEC 1)
2. **Add Logging**: Implement structured logging for debugging
3. **Add Monitoring**: Set up health check endpoint
4. **Prepare for SPEC 2**: Review JWT authentication integration plan
5. **Deploy**: Deploy to production environment (Heroku, AWS, etc.)

## Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Neon PostgreSQL Documentation: https://neon.tech/docs/
- OpenAPI Specification: See `contracts/openapi.yaml`
- Data Model: See `data-model.md`
- Research Findings: See `research.md`

## Support

For issues or questions:
- Check API documentation at http://localhost:8000/docs
- Review error messages in server logs
- Consult research.md for technical decisions
- Refer to data-model.md for schema details

# Backend REST API + Database

Task Management REST API built with FastAPI, SQLModel, and Neon Serverless PostgreSQL.

## Features

- Full CRUD operations for tasks
- User ownership enforcement (all queries scoped by user_id)
- Persistent storage in Neon PostgreSQL
- Automatic OpenAPI documentation
- Async/await for high concurrency

## Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL account (free tier available at https://neon.tech)

## Setup Instructions

### 1. Get Neon PostgreSQL Connection String

1. Sign up for Neon at https://neon.tech
2. Create a new project
3. Copy the **pooled connection string** (includes `?pgbouncer=true`)

### 2. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
DATABASE_URL=postgresql://user:password@host/database?sslmode=require&pgbouncer=true
```

Replace with your actual Neon connection string.

### 5. Run the API Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

### 6. View API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### List Tasks
```bash
GET /api/{user_id}/tasks
```

### Create Task
```bash
POST /api/{user_id}/tasks
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation"
}
```

### Get Single Task
```bash
GET /api/{user_id}/tasks/{task_id}
```

### Update Task
```bash
PUT /api/{user_id}/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": false
}
```

### Delete Task
```bash
DELETE /api/{user_id}/tasks/{task_id}
```

### Toggle Task Completion
```bash
PATCH /api/{user_id}/tasks/{task_id}/complete
```

## Project Structure

```
backend/
├── src/
│   ├── models/          # SQLModel entities
│   ├── schemas/         # Pydantic request/response schemas
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   ├── dependencies.py  # Dependency injection
│   └── main.py          # FastAPI app
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── README.md            # This file
```

## Development

### Running Tests

Tests are optional for this specification. To add tests:

```bash
pip install pytest pytest-asyncio httpx
pytest
```

### Database Migrations

For production, use Alembic for migrations:

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Create tasks table"
alembic upgrade head
```

## Troubleshooting

### Connection refused error
Verify Neon connection string is correct and database is accessible.

### Too many connections error
Use Neon's pooled connection string with `?pgbouncer=true`.

### Table does not exist error
Ensure database tables are created on startup (automatic with SQLModel).

## License

MIT

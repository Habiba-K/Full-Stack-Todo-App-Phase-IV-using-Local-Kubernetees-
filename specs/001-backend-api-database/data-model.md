# Data Model: Backend REST API + Database

**Feature**: Backend REST API + Database
**Date**: 2026-01-22
**Status**: Complete

## Overview

This document defines the data model for the task management REST API. The model is designed to support multi-user task management with user ownership enforcement at the database level.

## Entities

### Task

**Description**: Represents a single task item owned by a user. Tasks contain a title, optional description, completion status, and automatic timestamps.

**Attributes**:

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, AUTO-GENERATED | Unique identifier for the task |
| user_id | VARCHAR(255) | NOT NULL, INDEXED | Owner of the task (references user, but users table not in this spec) |
| title | VARCHAR(500) | NOT NULL | Task title (required, max 500 characters) |
| description | TEXT | NULLABLE | Optional task description (max 5000 characters) |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status of the task |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | When the task was created (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | When the task was last updated (UTC) |

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` for fast user-scoped queries

**Validation Rules**:
- `title` must not be empty or only whitespace
- `title` length: 1-500 characters
- `description` length: 0-5000 characters (optional)
- `user_id` must be provided (validated at application level)
- `completed` defaults to false if not specified
- `created_at` and `updated_at` are set automatically

**State Transitions**:
- **Created**: Task starts with `completed = false`
- **Completed**: Task can be marked `completed = true` via PATCH endpoint
- **Uncompleted**: Task can be marked `completed = false` via PATCH endpoint
- **Updated**: Any field change updates `updated_at` timestamp
- **Deleted**: Task is permanently removed (no soft delete in SPEC 1)

**Relationships**:
- **User** (1:N): Each task belongs to one user (user_id foreign key reference)
  - Note: Users table is out of scope for SPEC 1, will be added in SPEC 2
  - user_id is treated as a string identifier for now

## Database Schema (SQL)

```sql
-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast user-scoped queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## SQLModel Definition (Python)

```python
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    """
    Task entity representing a user's task item.

    Attributes:
        id: Unique identifier (UUID)
        user_id: Owner identifier (string, references user)
        title: Task title (required, max 500 chars)
        description: Optional task description (max 5000 chars)
        completed: Completion status (default: False)
        created_at: Creation timestamp (UTC)
        updated_at: Last update timestamp (UTC)
    """
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(max_length=255, index=True)
    title: str = Field(max_length=500)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Pydantic Schemas (API Contracts)

```python
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator

class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Attributes:
        title: Task title (required, 1-500 chars)
        description: Optional task description (max 5000 chars)
    """
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)

    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or only whitespace')
        return v.strip()

class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    All fields are optional for partial updates.

    Attributes:
        title: Updated task title (1-500 chars)
        description: Updated task description (max 5000 chars)
        completed: Updated completion status
    """
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    completed: Optional[bool] = None

    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty or only whitespace')
        return v.strip() if v else v

class TaskResponse(BaseModel):
    """
    Schema for task responses (read operations).
    Includes all fields including read-only ones.

    Attributes:
        id: Task unique identifier
        user_id: Task owner identifier
        title: Task title
        description: Task description (optional)
        completed: Completion status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: UUID
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Allow conversion from SQLModel objects
```

## Data Constraints and Business Rules

### Constraint 1: User Ownership
- **Rule**: All tasks must be associated with a user_id
- **Enforcement**: Application layer (service methods filter by user_id)
- **Validation**: user_id from URL path must match task's user_id
- **Error**: 404 Not Found if task doesn't belong to user

### Constraint 2: Title Required
- **Rule**: Every task must have a non-empty title
- **Enforcement**: Database NOT NULL constraint + Pydantic validation
- **Validation**: Title must be 1-500 characters, not only whitespace
- **Error**: 422 Validation Error if title is missing or invalid

### Constraint 3: Description Optional
- **Rule**: Description is optional and can be null
- **Enforcement**: Database NULLABLE + Pydantic Optional type
- **Validation**: If provided, max 5000 characters
- **Error**: 422 Validation Error if description exceeds limit

### Constraint 4: Completion Status
- **Rule**: Tasks have a boolean completion status
- **Enforcement**: Database BOOLEAN with DEFAULT FALSE
- **Validation**: Must be true or false (no null)
- **Error**: 422 Validation Error if invalid boolean value

### Constraint 5: Automatic Timestamps
- **Rule**: created_at and updated_at are managed automatically
- **Enforcement**: Database triggers + SQLModel defaults
- **Validation**: Clients cannot set these fields
- **Error**: Fields ignored if provided in create/update requests

### Constraint 6: Unique Task IDs
- **Rule**: Each task has a unique UUID identifier
- **Enforcement**: Database PRIMARY KEY constraint + UUID generation
- **Validation**: IDs are auto-generated, clients cannot set them
- **Error**: Database constraint violation if duplicate (unlikely with UUIDs)

## Query Patterns

### Pattern 1: List User Tasks
```python
# Get all tasks for a specific user
tasks = db.query(Task).filter(Task.user_id == user_id).all()
```
**Performance**: O(n) where n = number of tasks for user, optimized by index on user_id

### Pattern 2: Get Single Task
```python
# Get specific task for a user (ownership check)
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == user_id
).first()
```
**Performance**: O(1) with primary key + index lookup

### Pattern 3: Create Task
```python
# Create new task for user
task = Task(user_id=user_id, title=title, description=description)
db.add(task)
db.commit()
db.refresh(task)
```
**Performance**: O(1) single insert operation

### Pattern 4: Update Task
```python
# Update task with ownership check
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == user_id
).first()
if task:
    task.title = new_title
    task.description = new_description
    db.commit()
    db.refresh(task)
```
**Performance**: O(1) single update operation

### Pattern 5: Delete Task
```python
# Delete task with ownership check
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == user_id
).first()
if task:
    db.delete(task)
    db.commit()
```
**Performance**: O(1) single delete operation

### Pattern 6: Toggle Completion
```python
# Toggle completion status with ownership check
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == user_id
).first()
if task:
    task.completed = not task.completed
    db.commit()
    db.refresh(task)
```
**Performance**: O(1) single update operation

## Migration Strategy

### Initial Migration
```python
# Alembic migration: create tasks table
def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])

def downgrade():
    op.drop_index('idx_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
```

## Future Considerations (SPEC 2+)

### User Table Integration
- Add foreign key constraint: `user_id REFERENCES users(id)`
- Add ON DELETE CASCADE or SET NULL behavior
- Migrate existing user_id strings to UUID references

### Additional Fields
- `priority` (enum: low, medium, high)
- `due_date` (timestamp)
- `completed_at` (timestamp, set when completed=true)
- `deleted_at` (timestamp, for soft deletes)
- `tags` (array or separate table)

### Performance Optimizations
- Composite index on (user_id, completed) for filtered queries
- Composite index on (user_id, created_at) for sorted queries
- Pagination support (LIMIT/OFFSET or cursor-based)

### Data Integrity
- Add CHECK constraint: `title <> ''` (non-empty)
- Add CHECK constraint: `length(title) <= 500`
- Add CHECK constraint: `length(description) <= 5000`

## Testing Considerations

### Unit Tests (Data Model)
- Test Task model creation with valid data
- Test validation rules (title required, length limits)
- Test default values (completed=false, timestamps)
- Test UUID generation

### Integration Tests (Database)
- Test task creation and retrieval
- Test user ownership filtering
- Test concurrent updates (optimistic locking)
- Test index performance with large datasets

### Contract Tests (API Schemas)
- Test TaskCreate schema validation
- Test TaskUpdate schema validation
- Test TaskResponse serialization
- Test error responses for invalid data

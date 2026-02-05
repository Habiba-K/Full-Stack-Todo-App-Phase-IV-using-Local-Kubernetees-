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
        from_attributes = True  # Allow conversion from SQLModel objects

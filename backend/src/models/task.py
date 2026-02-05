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
        description: Optional task description
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

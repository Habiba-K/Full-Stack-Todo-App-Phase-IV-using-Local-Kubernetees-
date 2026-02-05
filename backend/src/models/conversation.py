from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation between a user and the AI agent.

    Attributes:
        id: Unique conversation identifier
        user_id: Foreign key to users table
        title: Auto-generated conversation title from first message
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last updated
    """
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

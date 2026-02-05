from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON, Text
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Any


class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation.

    Attributes:
        id: Unique message identifier
        conversation_id: Foreign key to conversations table
        role: Message role - either "user" or "assistant"
        content: Message text content
        tool_calls: JSON array of tool invocations (for assistant messages)
        created_at: Timestamp when message was created
    """
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(sa_column=Column(Text, nullable=False))
    tool_calls: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

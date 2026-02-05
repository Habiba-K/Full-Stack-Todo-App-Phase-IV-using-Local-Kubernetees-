from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from src.models.conversation import Conversation
from src.models.message import Message
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any


async def get_or_create_conversation(db: AsyncSession, user_id: UUID) -> Conversation:
    """
    Get the user's active conversation or create a new one.

    Args:
        db: Database session
        user_id: User's UUID

    Returns:
        Conversation object
    """
    # Check if user has an existing conversation
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(desc(Conversation.updated_at))
        .limit(1)
    )
    conversation = result.scalar_one_or_none()

    if conversation:
        return conversation

    # Create new conversation
    conversation = Conversation(
        user_id=user_id,
        title="New Conversation"
    )
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)

    return conversation


async def add_message(
    db: AsyncSession,
    conversation_id: UUID,
    role: str,
    content: str,
    tool_calls: Optional[List[Dict[str, Any]]] = None
) -> Message:
    """
    Add a message to a conversation.

    Args:
        db: Database session
        conversation_id: Conversation UUID
        role: Message role ("user" or "assistant")
        content: Message text content
        tool_calls: Optional list of tool invocations

    Returns:
        Created Message object
    """
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    db.add(message)

    # Update conversation's updated_at timestamp
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one()
    conversation.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(message)

    return message


async def get_recent_messages(
    db: AsyncSession,
    conversation_id: UUID,
    limit: int = 20
) -> List[Message]:
    """
    Get recent messages from a conversation for agent context.

    Args:
        db: Database session
        conversation_id: Conversation UUID
        limit: Maximum number of messages to retrieve

    Returns:
        List of Message objects, ordered by created_at ascending
    """
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(desc(Message.created_at))
        .limit(limit)
    )
    messages = result.scalars().all()

    # Reverse to get chronological order (oldest first)
    return list(reversed(messages))


async def get_conversation_history(
    db: AsyncSession,
    user_id: UUID,
    conversation_id: Optional[UUID] = None,
    limit: int = 50,
    before_id: Optional[UUID] = None
) -> tuple[Optional[UUID], List[Message], bool]:
    """
    Get conversation history with pagination support.

    Args:
        db: Database session
        user_id: User's UUID
        conversation_id: Optional specific conversation ID
        limit: Maximum messages to return
        before_id: Cursor for pagination (return messages before this ID)

    Returns:
        Tuple of (conversation_id, messages list, has_more boolean)
    """
    # Get conversation
    if conversation_id:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id, Conversation.user_id == user_id)
        )
        conversation = result.scalar_one_or_none()
    else:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.updated_at))
            .limit(1)
        )
        conversation = result.scalar_one_or_none()

    if not conversation:
        return None, [], False

    # Build query for messages
    query = select(Message).where(Message.conversation_id == conversation.id)

    # Apply cursor pagination if before_id is provided
    if before_id:
        before_message_result = await db.execute(
            select(Message).where(Message.id == before_id)
        )
        before_message = before_message_result.scalar_one_or_none()
        if before_message:
            query = query.where(Message.created_at < before_message.created_at)

    # Order by created_at descending and limit
    query = query.order_by(desc(Message.created_at)).limit(limit + 1)

    result = await db.execute(query)
    messages = result.scalars().all()

    # Check if there are more messages
    has_more = len(messages) > limit
    if has_more:
        messages = messages[:limit]

    # Reverse to get chronological order (oldest first)
    messages = list(reversed(messages))

    return conversation.id, messages, has_more

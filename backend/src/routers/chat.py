import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

from src.database import get_session
from src.auth.dependencies import get_current_user_id
from src.services import chat_service, agent_service

logger = logging.getLogger(__name__)


# Request/Response Schemas
class ChatRequest(BaseModel):
    """Request schema for sending a chat message."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    conversation_id: Optional[UUID] = Field(None, description="Optional conversation ID")


class MessageResponse(BaseModel):
    """Schema for a single message in responses."""
    id: UUID
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]]
    created_at: datetime


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    conversation_id: UUID
    message: MessageResponse


class ChatHistoryResponse(BaseModel):
    """Response schema for chat history endpoint."""
    conversation_id: Optional[UUID]
    messages: List[MessageResponse]
    has_more: bool


# Router
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    db: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id)
):
    """
    Send a message to the AI chat agent and receive a response.

    The agent will interpret the message, execute appropriate tools (task operations),
    and return a natural language response.
    """
    try:
        # Get or create conversation
        conversation = await chat_service.get_or_create_conversation(db, user_id)

        # Store user message
        user_message = await chat_service.add_message(
            db=db,
            conversation_id=conversation.id,
            role="user",
            content=request.message,
            tool_calls=None
        )

        # Load recent conversation history for agent context
        recent_messages = await chat_service.get_recent_messages(
            db=db,
            conversation_id=conversation.id,
            limit=settings.chat_context_messages - 1  # -1 because we'll add the new message
        )

        # Convert messages to format expected by agent
        conversation_history = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in recent_messages
        ]

        # Run agent
        agent_response, tool_calls = await agent_service.run_agent(
            user_id=str(user_id),
            conversation_messages=conversation_history,
            user_message=request.message,
            db=db
        )

        # Store assistant response
        assistant_message = await chat_service.add_message(
            db=db,
            conversation_id=conversation.id,
            role="assistant",
            content=agent_response,
            tool_calls=tool_calls
        )

        # Return response
        return ChatResponse(
            conversation_id=conversation.id,
            message=MessageResponse(
                id=assistant_message.id,
                role=assistant_message.role,
                content=assistant_message.content,
                tool_calls=assistant_message.tool_calls,
                created_at=assistant_message.created_at
            )
        )

    except Exception as e:
        logger.exception("Error processing chat message")
        raise HTTPException(
            status_code=500,
            detail="I'm having trouble processing your request. Please try again."
        )


@router.get("/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    conversation_id: Optional[UUID] = None,
    limit: int = 50,
    before: Optional[UUID] = None,
    db: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id)
):
    """
    Retrieve conversation history for the authenticated user.

    Supports pagination using the 'before' cursor parameter.
    """
    try:
        # Validate limit
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=422, detail="Limit must be between 1 and 100")

        # Get conversation history
        conv_id, messages, has_more = await chat_service.get_conversation_history(
            db=db,
            user_id=user_id,
            conversation_id=conversation_id,
            limit=limit,
            before_id=before
        )

        # Convert messages to response format
        message_responses = [
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                tool_calls=msg.tool_calls,
                created_at=msg.created_at
            )
            for msg in messages
        ]

        return ChatHistoryResponse(
            conversation_id=conv_id,
            messages=message_responses,
            has_more=has_more
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error retrieving conversation history")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve conversation history"
        )


# Import settings for chat_context_messages
from src.config import settings

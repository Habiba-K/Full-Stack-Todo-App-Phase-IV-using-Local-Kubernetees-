# Quickstart: AI Chat Agent with Groq Tool Calling

**Feature**: 005-ai-chat-agent | **Date**: 2026-01-29 | **Updated**: Spec-6/7 alignment

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- Neon PostgreSQL database (existing from previous features)
- Groq API key (free tier available at console.groq.com)
- Existing backend and frontend from Phase-II running

## Environment Setup

### 1. Backend Environment Variables

Add to `backend/.env`:

```env
# Existing variables (keep as-is)
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-here
CORS_ORIGINS=http://localhost:3000

# NEW: Groq Configuration
GROQ_API_KEY=gsk_your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
CHAT_CONTEXT_MESSAGES=50
```

### 2. Backend Dependencies

```bash
cd backend
pip install groq pydantic-settings
```

New dependencies added to `requirements.txt`:
- `groq` — Groq Python SDK for tool calling

### 3. Frontend Dependencies

No new frontend dependencies required. Uses existing fetch API for chat endpoint.

### 4. Database Migration

New tables are auto-created by SQLModel on startup (same pattern as existing tables):
- `conversations` — stores chat sessions per user
- `messages` — stores individual messages (user + assistant + tool calls)

## Running the Application

### Backend
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

### Access
- Chat UI: http://localhost:3000/chat (requires authentication)
- Dashboard: http://localhost:3000/dashboard (existing)
- API Docs: http://localhost:8000/docs

## Testing the Chat Agent

### 1. Sign in via the existing UI
Navigate to http://localhost:3000/signin and log in.

### 2. Open the Chat
Navigate to http://localhost:3000/chat.

### 3. Test Conversations

**Create a task:**
```
You: "Add a task to buy groceries"
Agent: "Done! I've created a task 'Buy groceries' for you."
```

**List tasks:**
```
You: "Show me my tasks"
Agent: "Here are your current tasks:
1. Buy groceries (pending)
2. Prepare presentation (completed)"
```

**Complete a task:**
```
You: "Mark buy groceries as done"
Agent: "Done! 'Buy groceries' has been marked as complete."
```

**Update a task:**
```
You: "Change the title of groceries task to 'Buy milk'"
Agent: "Updated! The task is now titled 'Buy milk'."
```

**Delete a task:**
```
You: "Delete the milk task"
Agent: "Done! 'Buy milk' has been deleted."
```

**Follow-up context:**
```
You: "Add task: finish report"
Agent: "Done! I've created 'Finish report' for you."
You: "Also set it to high priority"
Agent: "Updated! 'Finish report' is now high priority."
```

## API Testing (curl)

### Send a chat message
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### Response
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "role": "assistant",
    "content": "Done! I've created a task 'Buy groceries' for you.",
    "tool_calls": [
      {
        "tool": "add_task",
        "input": {"title": "Buy groceries"},
        "result": {"status": "success", "data": {"id": "...", "title": "Buy groceries"}}
      }
    ],
    "created_at": "2026-01-29T10:30:00Z"
  }
}
```

### Get conversation history
```bash
curl http://localhost:8000/api/chat/history \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Project File Map

| File | Purpose | New/Modified |
|------|---------|-------------|
| `backend/src/models/conversation.py` | Conversation SQLModel | New |
| `backend/src/models/message.py` | Message SQLModel | New |
| `backend/src/routers/chat.py` | Chat API endpoints | New |
| `backend/src/services/chat_service.py` | Conversation persistence | New |
| `backend/src/services/agent_service.py` | Groq agent orchestration | New |
| `backend/src/tools/__init__.py` | Tool registry | New |
| `backend/src/tools/task_tools.py` | Task tool definitions | New |
| `backend/src/tools/schemas.py` | Tool I/O schemas (Pydantic) | New |
| `backend/src/config.py` | Add GROQ_API_KEY setting | Modified |
| `backend/src/main.py` | Register chat router | Modified |
| `backend/requirements.txt` | Add groq dependency | Modified |
| `frontend/app/chat/page.tsx` | Chat page | New |
| `frontend/components/chat/ChatContainer.tsx` | Chat UI component | New |
| `frontend/components/chat/MessageBubble.tsx` | Message display | New |
| `frontend/components/chat/ChatInput.tsx` | Message input | New |
| `frontend/lib/chat.ts` | Chat API helpers | New |
| `frontend/types/chat.ts` | Chat type definitions | New |
| `frontend/middleware.ts` | Add /chat to protected routes | Modified |
| `backend/.env.example` | Add GROQ env vars | Modified |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                        │
│  ┌──────────────┐                                               │
│  │  /chat page  │ ──── fetch ───────────────────────────────────┼──┐
│  └──────────────┘                                               │  │
└─────────────────────────────────────────────────────────────────┘  │
                                                                     │
┌─────────────────────────────────────────────────────────────────┐  │
│                        Backend (FastAPI)                         │  │
│  ┌──────────────┐                                               │  │
│  │ POST /api/   │ ◄─────────────────────────────────────────────┼──┘
│  │    chat      │                                               │
│  └──────┬───────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │    chat_     │───►│    agent_    │───►│    tools/    │      │
│  │   service    │    │   service    │    │  task_tools  │      │
│  │ (persist)    │    │  (Groq SDK)  │    │  (Pydantic)  │      │
│  └──────┬───────┘    └──────────────┘    └──────┬───────┘      │
│         │                                        │              │
│         ▼                                        ▼              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                   task_service.py                       │    │
│  │               (existing CRUD logic)                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                  │
└──────────────────────────────┼──────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Neon PostgreSQL │
                    │  - users         │
                    │  - tasks         │
                    │  - conversations │
                    │  - messages      │
                    └──────────────────┘
```

## Stateless Request Flow

1. **Request arrives** at `POST /api/chat` with JWT token and message
2. **JWT validated** → extract `user_id`
3. **Load conversation** from database (or create new)
4. **Persist user message** to database immediately
5. **Build context** = system prompt + last N messages
6. **Call Groq** with tools, handle tool calls iteratively
7. **Persist assistant response** (with tool_calls) to database
8. **Return response** to client

**Key**: No in-memory state. Server can restart between requests without data loss.

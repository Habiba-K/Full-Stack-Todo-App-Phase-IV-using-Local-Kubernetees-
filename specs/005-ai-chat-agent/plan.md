# Implementation Plan: AI Chat Agent with MCP Server & Groq

**Branch**: `005-ai-chat-agent` | **Date**: 2026-01-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/005-ai-chat-agent/spec.md`

## Summary

Implement a stateless AI-powered Chat API that manages todo tasks through MCP tools hosted by the official MCP SDK. The system uses Groq SDK for the AI agent, which discovers and invokes tools via MCP protocol. All conversation context and task state persist in the database, ensuring the system survives server restarts without memory loss.

**Key Architectural Decisions**:
- Official MCP SDK for hosting tools as an MCP server
- Groq SDK for AI agent (not OpenAI Agents SDK)
- MCP server embedded in FastAPI application (not separate process)
- Completely stateless backend — conversation rebuilt from database on every request
- MCP tools wrap existing `task_service.py` — no direct database access from agent
- User context (user_id) passed as tool parameters

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, Groq SDK, Official MCP SDK, SQLModel, Pydantic
**Storage**: Neon Serverless PostgreSQL (existing database)
**Testing**: pytest (existing test framework)
**Target Platform**: Linux server / containerized deployment
**Project Type**: Web application (backend API + frontend)
**Performance Goals**: <3 seconds response time for simple operations
**Constraints**: Stateless backend, all state in database, user-scoped data isolation
**Scale/Scope**: Single active conversation per user, 50-message context window

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Security-First Design | ✅ PASS | User ID passed to all MCP tools, tools validate ownership |
| II. Stateless Architecture Mandate | ✅ PASS | No in-memory state, conversation rebuilt from DB per request |
| III. Clean Separation of Concerns | ✅ PASS | Agent (Groq) → MCP Server → Tools (Pydantic) → Service (SQLModel) → DB |
| IV. MCP Tool-Only Data Access | ✅ PASS | Official MCP SDK hosts tools, agent uses MCP protocol |
| V. Conversation-Driven Design | ✅ PASS | Natural language interface, agent interprets intent |
| VI. Database as Single Source of Truth | ✅ PASS | Conversations/messages persisted immediately |
| VII. Maintainability and Testability | ✅ PASS | MCP tools independently testable, Pydantic schemas |

**Gate Result**: PASS

## Project Structure

### Documentation (this feature)

```text
specs/005-ai-chat-agent/
├── plan.md              # This file
├── spec.md              # Feature specification (updated for MCP SDK)
├── research.md          # Phase 0 output - MCP SDK & Groq integration research
├── data-model.md        # Phase 1 output - Conversation/Message entities
├── quickstart.md        # Phase 1 output - Setup and testing guide
├── contracts/           # Phase 1 output - API contracts
│   └── chat-api.md      # Chat endpoint specifications
└── tasks.md             # Phase 2 output - Implementation tasks
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py    # NEW: Conversation SQLModel
│   │   └── message.py         # NEW: Message SQLModel
│   ├── routers/
│   │   └── chat.py            # NEW: Chat API endpoints
│   ├── services/
│   │   ├── chat_service.py    # NEW: Conversation persistence
│   │   └── agent_service.py   # NEW: Groq agent orchestration
│   ├── mcp/
│   │   ├── __init__.py        # NEW: MCP server initialization
│   │   ├── server.py          # NEW: MCP server setup with official SDK
│   │   ├── tools.py           # NEW: MCP tool implementations
│   │   └── schemas.py         # NEW: Tool I/O Pydantic schemas
│   ├── config.py              # MODIFIED: Add GROQ and MCP settings
│   └── main.py                # MODIFIED: Initialize MCP server, register chat router
├── requirements.txt           # MODIFIED: Add groq and mcp dependencies
└── tests/
    ├── unit/
    │   └── test_mcp_tools.py  # NEW: MCP tool unit tests
    └── integration/
        └── test_chat.py       # NEW: Chat API integration tests

frontend/
├── app/
│   └── chat/
│       └── page.tsx           # NEW: Chat page
├── components/
│   └── chat/
│       ├── ChatContainer.tsx  # NEW: Main chat component
│       ├── MessageBubble.tsx  # NEW: Message display
│       └── ChatInput.tsx      # NEW: Message input
├── lib/
│   └── chat.ts                # NEW: Chat API helpers
├── types/
│   └── chat.ts                # NEW: Chat type definitions
└── middleware.ts              # MODIFIED: Add /chat to protected routes
```

**Structure Decision**: New `mcp/` directory for MCP server and tools, separated from services layer. MCP server runs embedded in FastAPI application.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP SDK + Groq (not OpenAI Agents) | Requirement specifies Groq for AI agent with official MCP SDK for tools | OpenAI Agents SDK would require different architecture and API costs |
| Embedded MCP server | Simplifies deployment and reduces operational complexity | Separate MCP server process would require inter-process communication and additional infrastructure |

## Implementation Phases

### Phase 0: Research & Dependencies

**Goal**: Research MCP SDK integration patterns and add dependencies

1. **Research MCP SDK** (`specs/005-ai-chat-agent/research.md`)
   - Official MCP SDK Python package installation
   - MCP server initialization patterns
   - Tool registration with `@mcp.tool()` decorator or equivalent
   - MCP protocol for tool discovery and invocation
   - Integration patterns with Groq SDK

2. **Update dependencies** (`backend/requirements.txt`)
   - Add `mcp` (official MCP SDK)
   - Add `groq` (Groq SDK)
   - Verify compatibility with existing packages

### Phase 1: Database Models & Persistence

**Goal**: Create database tables for conversations and messages

1. **Conversation model** (`backend/src/models/conversation.py`)
   - Fields: id (UUID), user_id (FK), title, created_at, updated_at
   - Index on user_id for fast lookup

2. **Message model** (`backend/src/models/message.py`)
   - Fields: id (UUID), conversation_id (FK), role (enum: user/assistant), content, tool_calls (JSON), created_at
   - Index on conversation_id + created_at for efficient history loading

3. **Chat service** (`backend/src/services/chat_service.py`)
   - `get_or_create_conversation(user_id)` — get active conversation or create new
   - `add_message(conversation_id, role, content, tool_calls)` — persist message
   - `get_messages(conversation_id, limit)` — load recent messages for context
   - `update_conversation_timestamp(conversation_id)` — update last activity

### Phase 2: MCP Server Setup (Official SDK)

**Goal**: Set up MCP server with official SDK and register tools

1. **MCP server initialization** (`backend/src/mcp/server.py`)
   - Import official MCP SDK
   - Create MCP server instance
   - Configure server settings (name, version, capabilities)
   - Implement server lifecycle management (start, stop)

2. **Tool schemas** (`backend/src/mcp/schemas.py`)
   - Input schemas using Pydantic: AddTaskInput, ListTasksInput, GetTaskInput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput
   - Output schemas: TaskResponse, TaskListResponse, ErrorResponse
   - Validation rules (required fields, string lengths, enums)

3. **MCP tool implementations** (`backend/src/mcp/tools.py`)
   - `add_task(user_id, title, description?)` → TaskResponse
   - `list_tasks(user_id, status?)` → TaskListResponse
   - `get_task(user_id, task_id)` → TaskResponse
   - `update_task(user_id, task_id, title?, description?)` → TaskResponse
   - `complete_task(user_id, task_id)` → TaskResponse
   - `delete_task(user_id, task_id)` → TaskResponse
   - Each tool wraps `task_service` functions
   - Each tool validates user ownership
   - Each tool returns structured responses
   - Each tool handles errors gracefully (task not found, validation errors)

4. **Tool registration** (`backend/src/mcp/__init__.py`)
   - Register all tools with MCP server using official SDK decorators/methods
   - Export MCP server instance for use in FastAPI app
   - Implement tool discovery endpoint (if required by MCP protocol)

### Phase 3: Groq Agent Service

**Goal**: Implement Groq-based agent with MCP tool integration

1. **Config updates** (`backend/src/config.py`)
   - Add GROQ_API_KEY, GROQ_MODEL settings
   - Add CHAT_CONTEXT_MESSAGES (default: 50)
   - Add MCP_SERVER_URL (if needed for connection)

2. **Agent service** (`backend/src/services/agent_service.py`)
   - Initialize Groq client with API key
   - Connect to MCP server (embedded or via protocol)
   - Discover available MCP tools from server
   - Convert MCP tool schemas to Groq tool format
   - `run_agent(user_id, messages, db)` — main agent loop
   - System prompt with task management instructions
   - Handle tool calls iteratively until final response
   - Invoke MCP tools via MCP protocol
   - Return AgentResult(content, tool_calls_metadata)

3. **Error handling**
   - Catch MCP tool exceptions → structured error responses
   - Catch Groq API errors → user-friendly error messages
   - Catch MCP server connection errors → graceful degradation
   - Log errors without exposing to user

### Phase 4: Chat API Endpoints

**Goal**: Implement REST endpoints for chat

1. **Chat router** (`backend/src/routers/chat.py`)
   - `POST /api/chat` — send message, get agent response
   - `GET /api/chat/history` — retrieve conversation history

2. **Request flow** (POST /api/chat):
   - Validate JWT → extract user_id
   - Load/create conversation
   - Persist user message
   - Build context (system prompt + history)
   - Execute Groq agent with MCP tools
   - Persist assistant response
   - Return response with tool_calls metadata

3. **Register router** in `main.py`
   - Initialize MCP server on app startup
   - Register chat router
   - Add shutdown handler for MCP server cleanup

### Phase 5: Frontend Chat UI

**Goal**: Build chat interface in Next.js

1. **Chat page** (`frontend/app/chat/page.tsx`)
   - Protected route (requires auth)
   - Load conversation history on mount
   - Send messages to API
   - Display responses with loading states

2. **Components**
   - `ChatContainer` — main layout with message list and input
   - `MessageBubble` — styled message display (user/assistant)
   - `ChatInput` — text input with send button

3. **API helpers** (`frontend/lib/chat.ts`)
   - `sendMessage(message)` — POST to /api/chat
   - `getHistory()` — GET /api/chat/history

4. **Types** (`frontend/types/chat.ts`)
   - ChatMessage, ChatResponse, Conversation types

5. **Middleware update** — add `/chat` to protected routes

### Phase 6: Testing & Validation

**Goal**: Verify all acceptance criteria

1. **MCP tool unit tests** (`backend/tests/unit/test_mcp_tools.py`)
   - Test each MCP tool with valid/invalid inputs
   - Verify structured response format
   - Verify user ownership validation
   - Test error handling (task not found, validation errors)
   - Test tools independently from agent

2. **Integration tests** (`backend/tests/integration/test_chat.py`)
   - Test chat endpoint end-to-end
   - Test conversation persistence
   - Test MCP tool execution through Groq agent
   - Test error handling
   - Test multi-turn conversations

3. **Manual validation**
   - Test all user stories from spec
   - Verify conversation continuity after server restart
   - Verify user data isolation
   - Test MCP server tool discovery
   - Test Groq agent tool selection accuracy

## Success Criteria Mapping

| Spec Criterion | Implementation |
|----------------|----------------|
| SC-001: Manage tasks via chat | MCP tools + Groq agent handle all CRUD operations |
| SC-002: Context persists 5+ messages | chat_service loads last 50 messages |
| SC-003: Survives server restart | All state in PostgreSQL, no in-memory cache |
| SC-004: Tools-only data access | MCP tools wrap task_service, agent has no DB access |
| SC-005: Consistent tool responses | Pydantic schemas enforce structured responses |
| SC-006: User-friendly errors | Agent translates MCP tool errors to natural language |
| SC-007: User data isolation | user_id passed to all MCP tools, validated on every operation |
| SC-008: 90% intent accuracy | Groq llama-3.3-70b-versatile with clear MCP tool descriptions |
| SC-009: Independent tool testing | MCP tools testable via direct invocation |
| SC-010: MCP server registration | Official SDK registers tools, discoverable by agent |

## MCP Server Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ FastAPI Application                                         │
│                                                             │
│  ┌──────────────────┐         ┌──────────────────────┐    │
│  │ Chat Endpoint    │────────▶│ Groq Agent Service   │    │
│  │ POST /api/chat   │         │ (Groq SDK)           │    │
│  └──────────────────┘         └──────────┬───────────┘    │
│                                           │                 │
│                                           │ MCP Protocol    │
│                                           ▼                 │
│                               ┌──────────────────────────┐ │
│                               │ MCP Server               │ │
│                               │ (Official MCP SDK)       │ │
│                               │                          │ │
│                               │ Tools:                   │ │
│                               │ - add_task               │ │
│                               │ - list_tasks             │ │
│                               │ - get_task               │ │
│                               │ - update_task            │ │
│                               │ - complete_task          │ │
│                               │ - delete_task            │ │
│                               └──────────┬───────────────┘ │
│                                          │                  │
│                                          ▼                  │
│                               ┌──────────────────────────┐ │
│                               │ Task Service             │ │
│                               │ (SQLModel)               │ │
│                               └──────────┬───────────────┘ │
│                                          │                  │
└──────────────────────────────────────────┼──────────────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │ Neon PostgreSQL │
                                  │ - tasks         │
                                  │ - conversations │
                                  │ - messages      │
                                  └─────────────────┘
```

## Dependencies

- **Existing**: FastAPI app, task_service.py, user authentication (JWT)
- **New**:
  - `mcp` — Official MCP SDK Python package
  - `groq` — Groq SDK for AI agent
- **External**:
  - Groq API key with tool calling access
  - MCP protocol support in Groq SDK (or adapter layer)

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| MCP SDK integration complexity | Research phase to understand SDK patterns, follow official examples |
| Groq + MCP protocol compatibility | Implement adapter layer if needed to translate between formats |
| Groq API rate limits | Implement retry with exponential backoff |
| Model hallucination | Clear system prompt, structured MCP tool responses |
| Large conversation context | Bounded message window (50 messages) |
| MCP tool execution failures | Structured error handling, user-friendly messages |
| MCP server startup failures | Graceful degradation, clear error logging |

## Key Implementation Requirements

### 1. Set up MCP server using Official MCP SDK ✅
- Use official `mcp` Python package
- Initialize MCP server in `backend/src/mcp/server.py`
- Embed server in FastAPI application lifecycle

### 2. Define tool schemas and parameters ✅
- JSON Schema definitions for each tool
- Pydantic models in `backend/src/mcp/schemas.py`
- Parameter validation (required fields, types, constraints)

### 3. Implement input validation per tool ✅
- Pydantic schema validation before execution
- Return structured error responses for invalid inputs
- Validate user_id, task_id, and other parameters

### 4. Enforce user-level task ownership ✅
- user_id required parameter for all tools
- Validate ownership before any operation
- Filter results by user_id

### 5. Execute database operations via SQLModel ✅
- MCP tools wrap existing `task_service.py` functions
- SQLModel ORM for all database operations
- No raw SQL queries in tools

### 6. Return structured tool responses ✅
- Consistent response schema: task_id, status, title
- Success responses with data
- Error responses with error type and message

### 7. Handle task-not-found and invalid input errors ✅
- Catch exceptions in tool implementations
- Return structured error responses
- Agent translates errors to user-friendly messages

### 8. Register tools with MCP runtime ✅
- Use official MCP SDK registration methods
- Tools discoverable via MCP protocol
- Tool metadata (name, description, parameters) exposed

### 9. Test tools independently from agent ✅
- Unit tests for each MCP tool
- Direct tool invocation without agent
- Verify structured responses for all scenarios

## Next Steps

Run `/sp.tasks` to generate detailed implementation tasks from this plan.

# Tasks: AI Chat Agent with MCP Server & Groq

**Input**: Design documents from `/specs/005-ai-chat-agent/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/chat-api.md

**Architecture**: Official MCP SDK server hosting tools, Groq SDK for AI agent

**Tests**: Unit tests for MCP tools, integration tests for chat API

**Organization**: Tasks grouped by phase to enable sequential implementation and testing.

## Format: `[ID] [P?] [Phase] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Phase]**: Which implementation phase this task belongs to
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/` (FastAPI + Python)
- **Frontend**: `frontend/` (Next.js + TypeScript)
- **Tests**: `backend/tests/` (pytest)
- **MCP**: `backend/src/mcp/` (MCP server and tools)

---

## Phase 0: Research & Dependencies

**Purpose**: Research MCP SDK integration and add required dependencies

- [x] T001 Research official MCP SDK Python package installation and basic usage patterns
- [x] T002 Research MCP server initialization and tool registration methods
- [x] T003 Research MCP protocol for tool discovery and invocation
- [x] T004 Research Groq SDK integration with MCP tools (adapter layer if needed)
- [x] T005 Add `mcp` package to backend/requirements.txt (official MCP SDK)
- [x] T006 [P] Add GROQ_API_KEY, GROQ_MODEL, CHAT_CONTEXT_MESSAGES settings to backend/src/config.py
- [x] T007 [P] Update backend/.env.example with GROQ_API_KEY and MCP settings

**Checkpoint**: ✅ Research complete, dependencies added

---

## Phase 1: Database Models & Persistence (Foundational)

**Purpose**: Core infrastructure for conversation persistence (required by ALL user stories)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [x] T008 [P] Create Conversation model in backend/src/models/conversation.py per data-model.md
- [x] T009 [P] Create Message model in backend/src/models/message.py per data-model.md
- [x] T010 Export new models in backend/src/main.py (imports trigger table creation)

### Chat Service (Conversation Persistence)

- [x] T011 Create chat_service.py in backend/src/services/ with get_or_create_conversation function
- [x] T012 Add add_message function to backend/src/services/chat_service.py
- [x] T013 Add get_messages function (with limit parameter) to backend/src/services/chat_service.py
- [x] T014 Add get_conversation_history function to backend/src/services/chat_service.py

**Checkpoint**: ✅ Foundation ready - conversation persistence complete

---

## Phase 2: MCP Server Setup (Official SDK)

**Purpose**: Set up MCP server with official SDK and implement tools

**⚠️ CRITICAL**: This phase must complete before agent integration

### MCP Server Infrastructure

- [x] T015 Create backend/src/mcp/__init__.py with MCP server initialization
- [x] T016 Create backend/src/mcp/server.py with MCP server setup using official SDK
- [x] T017 Implement MCP server lifecycle management (startup, shutdown) in server.py
- [x] T018 Configure MCP server settings (name, version, capabilities)

### Tool Schemas (Pydantic)

- [x] T019 Create backend/src/mcp/schemas.py with Pydantic input schemas
- [x] T020 [P] Create AddTaskInput schema with validation (title required, description optional)
- [x] T021 [P] Create ListTasksInput schema with status filter and limit
- [x] T022 [P] Create GetTaskInput schema with task_id validation
- [x] T023 [P] Create UpdateTaskInput schema with optional fields
- [x] T024 [P] Create CompleteTaskInput schema with task_id
- [x] T025 [P] Create DeleteTaskInput schema with task_id
- [x] T026 [P] Create TaskResponse, TaskListResponse, ErrorResponse output schemas

### MCP Tool Implementations

- [x] T027 Create backend/src/mcp/tools.py with tool implementations
- [x] T028 Implement add_task tool wrapping task_service.create_task
- [x] T029 Implement list_tasks tool wrapping task_service.get_user_tasks with filtering
- [x] T030 Implement get_task tool wrapping task_service.get_task_by_id
- [x] T031 Implement update_task tool wrapping task_service.update_task
- [x] T032 Implement complete_task tool wrapping task_service.toggle_task_completion
- [x] T033 Implement delete_task tool wrapping task_service.delete_task
- [x] T034 Add user ownership validation to all tools (verify user_id matches)
- [x] T035 Add error handling to all tools (task not found, validation errors)
- [x] T036 Ensure all tools return structured responses (task_id, status, title)

### Tool Registration with MCP Server

- [x] T037 Register all tools with MCP server using official SDK decorators/methods
- [x] T038 Implement tool discovery mechanism (if required by MCP protocol)
- [x] T039 Export MCP server instance from backend/src/mcp/__init__.py
- [x] T040 Add MCP server initialization to FastAPI app startup in backend/src/main.py
- [x] T041 Add MCP server shutdown handler to FastAPI app in backend/src/main.py

**Checkpoint**: ✅ MCP server operational - tools registered and discoverable

---

## Phase 3: Groq Agent Service (MCP Integration)

**Purpose**: Implement Groq-based agent that discovers and invokes MCP tools

### Agent Service Implementation

- [x] T042 Create agent_service.py in backend/src/services/ with Groq client initialization
- [x] T043 Implement MCP server connection in agent_service.py (embedded or via protocol)
- [x] T044 Implement tool discovery from MCP server in agent_service.py
- [x] T045 Implement MCP tool schema to Groq tool format conversion
- [x] T046 Create system prompt constant for task management assistant
- [x] T047 Implement run_agent function with tool execution loop in agent_service.py
- [x] T048 Add MCP tool invocation via MCP protocol in run_agent
- [x] T049 Add error handling for MCP tool exceptions in agent_service.py
- [x] T050 Add error handling for Groq API errors in agent_service.py
- [x] T051 Add error handling for MCP server connection errors in agent_service.py

**Checkpoint**: ✅ Agent service complete - Groq agent can discover and invoke MCP tools

---

## Phase 4: Chat API Endpoints

**Purpose**: Implement REST endpoints for chat with MCP tool integration

### Chat Router Implementation

- [x] T052 Create chat router in backend/src/routers/chat.py with POST /api/chat endpoint
- [x] T053 Implement chat endpoint request flow: validate JWT → load conversation → persist user message
- [x] T054 Integrate Groq agent with MCP tools in chat endpoint
- [x] T055 Persist assistant response with tool_calls metadata
- [x] T056 Return response with conversation_id and tool_calls
- [x] T057 Add GET /api/chat/history endpoint to backend/src/routers/chat.py
- [x] T058 Register chat router in backend/src/main.py

**Checkpoint**: ✅ Chat API operational - can create tasks via chat with MCP tools

---

## Phase 5: Frontend Chat UI

**Purpose**: Build chat interface in Next.js (unchanged from original plan)

### Types and API Helpers

- [x] T059 [P] Create frontend/types/chat.ts with ChatMessage, ChatResponse, Conversation types
- [x] T060 [P] Create frontend/lib/chat.ts with sendMessage API helper
- [x] T061 [P] Add getHistory API helper to frontend/lib/chat.ts

### Chat Components

- [x] T062 [P] Create ChatInput component in frontend/components/chat/ChatInput.tsx
- [x] T063 [P] Create MessageBubble component in frontend/components/chat/MessageBubble.tsx
- [x] T064 Create ChatContainer component in frontend/components/chat/ChatContainer.tsx
- [x] T065 Add loading state to ChatContainer
- [x] T066 Add error display to ChatContainer for API failures
- [x] T067 Add empty state message when no conversation history exists

### Chat Page

- [x] T068 Create chat page in frontend/app/chat/page.tsx (client component with useEffect for history)
- [x] T069 Update frontend/middleware.ts to protect /chat route

**Checkpoint**: ✅ Frontend complete - full chat UI operational

---

## Phase 6: Testing & Validation

**Purpose**: Verify all acceptance criteria and MCP tool functionality

### MCP Tool Unit Tests

- [ ] T070 [P] Create backend/tests/unit/test_mcp_tools.py test file
- [ ] T071 [P] Test add_task tool with valid and invalid inputs
- [ ] T072 [P] Test list_tasks tool with status filters
- [ ] T073 [P] Test get_task tool with valid and non-existent task_id
- [ ] T074 [P] Test update_task tool with various field combinations
- [ ] T075 [P] Test complete_task tool
- [ ] T076 [P] Test delete_task tool
- [ ] T077 [P] Verify all tools return structured responses (task_id, status, title)
- [ ] T078 [P] Verify user ownership validation in all tools
- [ ] T079 [P] Test error handling for task not found scenarios
- [ ] T080 [P] Test tools independently without agent (direct invocation)

### Integration Tests

- [ ] T081 [P] Create backend/tests/integration/test_chat.py test file
- [ ] T082 Test POST /api/chat endpoint end-to-end with task creation
- [ ] T083 Test conversation persistence across multiple requests
- [ ] T084 Test MCP tool execution through Groq agent
- [ ] T085 Test multi-turn conversations with context
- [ ] T086 Test error handling in chat endpoint
- [ ] T087 Test user data isolation (cannot access other users' tasks)

### Manual Validation

- [ ] T088 Test all user stories from spec.md manually
- [ ] T089 Verify conversation continuity after server restart
- [ ] T090 Verify MCP server tool discovery works correctly
- [ ] T091 Verify Groq agent tool selection accuracy
- [ ] T092 Run quickstart.md validation - test all conversation examples

**Checkpoint**: ✅ All tests passing - system ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 0: Research & Dependencies ────────────┐
                                             │
Phase 1: Database Models & Persistence ──────┤ (BLOCKS all subsequent phases)
                                             │
Phase 2: MCP Server Setup ───────────────────┤ (BLOCKS agent and API)
                                             │
Phase 3: Groq Agent Service ─────────────────┤ (BLOCKS API endpoints)
                                             │
Phase 4: Chat API Endpoints ─────────────────┤
                                             │
Phase 5: Frontend Chat UI ───────────────────┤ (Can start after Phase 4)
                                             │
Phase 6: Testing & Validation ───────────────┘
```

### Critical Path

1. **Phase 0** → Research MCP SDK patterns (T001-T007)
2. **Phase 1** → Database models and chat service (T008-T014)
3. **Phase 2** → MCP server setup and tool implementation (T015-T041)
4. **Phase 3** → Groq agent with MCP integration (T042-T051)
5. **Phase 4** → Chat API endpoints (T052-T058)
6. **Phase 5** → Frontend UI (T059-T069)
7. **Phase 6** → Testing (T070-T092)

### Parallel Opportunities

**Phase 0**: T001-T004 (research) can run in parallel, T005-T007 (config) can run in parallel

**Phase 1**: T008-T009 (models) can run in parallel, T011-T014 (chat service) are sequential

**Phase 2**:
- T020-T026 (schemas) can run in parallel after T019
- T028-T036 (tool implementations) can run in parallel after T027
- T037-T041 (registration) are sequential

**Phase 5**: T059-T063 (types, helpers, components) can run in parallel, T064-T069 are sequential

**Phase 6**: T070-T080 (unit tests) can run in parallel, T081-T087 (integration tests) can run in parallel

---

## Key Differences from Original Implementation

### What Changed (MCP SDK Integration)

1. **Tool Hosting**: Tools now hosted by official MCP SDK server (not direct Groq tool calling)
2. **Tool Registration**: Tools registered with MCP server using SDK decorators/methods
3. **Agent Integration**: Groq agent discovers tools from MCP server via MCP protocol
4. **Tool Invocation**: Agent invokes tools via MCP protocol (not direct function calls)
5. **Project Structure**: New `backend/src/mcp/` directory for MCP server and tools
6. **Dependencies**: Added official `mcp` package to requirements.txt
7. **Testing**: MCP tools can be tested independently from agent

### What Stayed the Same (No UI Impact)

1. **Frontend**: All frontend components, pages, and API helpers unchanged
2. **Database Models**: Conversation and Message models unchanged
3. **Chat Service**: Conversation persistence logic unchanged
4. **API Endpoints**: Chat API endpoints unchanged (POST /api/chat, GET /api/chat/history)
5. **Authentication**: JWT authentication flow unchanged
6. **User Experience**: Natural language interface and conversation flow unchanged

---

## Implementation Strategy

### Recommended Approach: Sequential by Phase

1. **Phase 0**: Complete research and add dependencies (7 tasks)
2. **Phase 1**: Complete database foundation (7 tasks)
3. **Phase 2**: Complete MCP server setup (27 tasks) - LARGEST PHASE
4. **Phase 3**: Complete Groq agent integration (10 tasks)
5. **Phase 4**: Complete Chat API (7 tasks)
6. **Phase 5**: Complete Frontend UI (11 tasks)
7. **Phase 6**: Complete Testing (23 tasks)

**Total Tasks**: 92 tasks

### Milestone Tracking

| Milestone | Tasks | Cumulative | Value Delivered | Status |
|-----------|-------|------------|-----------------|--------|
| Research | T001-T007 | 7 | MCP SDK patterns understood | ⏳ Pending |
| Foundation | T008-T014 | 14 | Conversation persistence ready | ⏳ Pending |
| MCP Server | T015-T041 | 41 | MCP tools operational | ⏳ Pending |
| Agent | T042-T051 | 51 | Groq agent with MCP integration | ⏳ Pending |
| API | T052-T058 | 58 | Chat API endpoints working | ⏳ Pending |
| Frontend | T059-T069 | 69 | Full chat UI operational | ⏳ Pending |
| Testing | T070-T092 | 92 | Production-ready system | ⏳ Pending |

---

## Success Criteria Verification

After implementation, verify these criteria from spec.md:

- [ ] **SC-001**: Users can manage tasks entirely through natural-language chat
- [ ] **SC-002**: Conversation context persists across 5+ stateless requests
- [ ] **SC-003**: System survives server restart with zero data loss
- [ ] **SC-004**: All task mutations flow through MCP tool invocations only
- [ ] **SC-005**: All MCP tool responses follow consistent structured schema
- [ ] **SC-006**: All errors result in user-friendly messages (no stack traces)
- [ ] **SC-007**: No user can access another user's tasks
- [ ] **SC-008**: Agent correctly identifies intent 90%+ of the time
- [ ] **SC-009**: MCP tools testable independently from agent
- [ ] **SC-010**: MCP server successfully registers all tools

---

## Notes

- MCP server runs embedded in FastAPI application (not separate process)
- All tools require user_id parameter for ownership validation
- Tools wrap existing task_service.py - no new database logic needed
- Agent has no direct DB access - all operations through MCP tools
- All state in PostgreSQL - survives server restart
- Frontend unchanged - no impact on UI/UX
- Commit after each phase or logical group of tasks

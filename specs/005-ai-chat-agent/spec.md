# Feature Specification: Chat API with MCP Server & Groq Agent

**Feature Branch**: `005-ai-chat-agent`
**Created**: 2026-01-28
**Updated**: 2026-01-29
**Status**: Draft - MCP SDK Integration
**Input**: Conversational interface for task management using Official MCP SDK server with Groq AI agent

## Architecture Overview

```
┌─────────────────┐ ┌──────────────────────────────────────────────┐ ┌─────────────────┐
│                 │ │ FastAPI Server                               │ │                 │
│                 │ │ ┌────────────────────────────────────────┐   │ │                 │
│  ChatKit UI     │─▶│ │ Chat Endpoint                          │   │ │   Neon DB       │
│  (Frontend)     │ │ │ POST /api/chat                         │   │ │ (PostgreSQL)    │
│                 │ │ └───────────────┬────────────────────────┘   │ │                 │
│                 │ │                 │                             │ │ - tasks         │
│                 │ │                 ▼                             │ │ - conversations │
│                 │ │ ┌────────────────────────────────────────┐   │ │ - messages      │
│                 │◀─│ │ Groq Agent                             │   │ │                 │
│                 │ │ │ (AI with tool calling)                 │   │ │                 │
│                 │ │ └───────────────┬────────────────────────┘   │ │                 │
│                 │ │                 │                             │ │                 │
│                 │ │                 ▼                             │ │                 │
│                 │ │ ┌────────────────────────────────────────┐   │─▶│                 │
│                 │ │ │ MCP Server (Official MCP SDK)          │   │ │                 │
│                 │ │ │ (MCP Tools for Task Operations)        │   │◀─│                 │
│                 │ │ └────────────────────────────────────────┘   │ │                 │
└─────────────────┘ └──────────────────────────────────────────────┘ └─────────────────┘
```

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Creation via Chat API (Priority: P1)

An authenticated user sends a natural-language message to the Chat API such as "Add a task to buy groceries by Friday." The backend receives the message, loads conversation history from the database, sends the full context to the Groq AI agent, which selects and invokes the appropriate MCP tool. The MCP server executes the tool, creates the task in the database, returns structured results to the agent, which formulates a confirmation response. Both the user message and agent response are persisted to the conversation record.

**Why this priority**: This is the core value loop — a user sends a message, the AI interprets it, invokes an MCP tool, mutates task state, and responds. Every other feature depends on this pipeline working end-to-end.

**Independent Test**: Send a POST request to the chat endpoint with a task creation message. Verify the response contains a confirmation, the task exists in the database scoped to the user, and both messages are persisted in the conversation history.

**Acceptance Scenarios**:

1. **Given** an authenticated user sends "Add a task to buy groceries by Friday" to the Chat API, **When** the agent processes the message, **Then** a task with title "Buy groceries" is created in the database for that user via the add_task MCP tool, and the API returns a confirmation message with the task details.
2. **Given** an authenticated user sends "I need to remember to pay bills", **When** the agent processes the message, **Then** a task with title "Pay bills" is created via MCP tool, and the response confirms the creation.
3. **Given** an authenticated user sends an ambiguous message like "groceries", **When** the agent cannot determine clear intent, **Then** the API returns a clarifying question such as "Would you like to create a task called 'Groceries'?"

---

### User Story 2 - Chat-Based Task Listing and Querying (Priority: P2)

An authenticated user sends a query message to the Chat API such as "Show me my tasks" or "What's pending?" The backend loads conversation context, the Groq agent selects the list_tasks MCP tool with appropriate filters, the MCP server retrieves the user's tasks from the database, and returns them to the agent which formats a summary. The exchange is persisted.

**Why this priority**: Viewing tasks completes the read side of the CRUD cycle and is the second most common interaction after creation.

**Independent Test**: Create tasks via the standard API, then send a list request through the Chat API. Verify the response includes correct task data and the conversation is persisted.

**Acceptance Scenarios**:

1. **Given** a user with 3 pending tasks, **When** they send "Show me all my tasks" to the Chat API, **Then** the response contains a formatted list of all 3 tasks with titles, statuses, and completion state.
2. **Given** a user with pending and completed tasks, **When** they send "What's pending?", **Then** the response shows only pending tasks via list_tasks MCP tool with status filter.
3. **Given** a user with no tasks, **When** they send "Show my tasks", **Then** the response contains a friendly message like "You don't have any tasks yet. Want to create one?"

---

### User Story 3 - Chat-Based Task Updates and Completion (Priority: P2)

An authenticated user sends an update request such as "Mark task 3 as complete" or "Change task 1 to 'Call mom tonight'." The agent identifies the target task via MCP tool invocation, the MCP server performs the update in the database, and returns confirmation which the agent formats into a user-friendly response.

**Why this priority**: Update and completion operations round out the core task management experience through chat.

**Independent Test**: Create a task, send an update/complete command through the Chat API, verify the task state changes in the database and the response confirms the action.

**Acceptance Scenarios**:

1. **Given** a user with a pending task with id=3, **When** they send "Mark task 3 as complete", **Then** the task status changes to completed in the database via complete_task MCP tool and the response confirms the completion.
2. **Given** a user with a task with id=1, **When** they send "Change task 1 to 'Call mom tonight'", **Then** the task's title is updated via update_task MCP tool and the response confirms the change.
3. **Given** a user sends "I finished the groceries task" without specifying task ID, **When** the agent needs to identify which task, **Then** the agent uses list_tasks first to find matching tasks, then calls complete_task.

---

### User Story 4 - Chat-Based Task Deletion (Priority: P3)

An authenticated user sends a delete request such as "Delete task 2" or "Remove the meeting task." The agent identifies the task, the MCP server performs the deletion, and the API returns a confirmation.

**Why this priority**: Deletion is a less frequent operation but necessary for complete task lifecycle management.

**Independent Test**: Create a task, send a delete command through the Chat API, verify the task is removed from the database and the response confirms deletion.

**Acceptance Scenarios**:

1. **Given** a user with a task with id=2, **When** they send "Delete task 2", **Then** the task is deleted from the database via delete_task MCP tool and the response confirms deletion.
2. **Given** a user references a task that doesn't exist, **When** the agent cannot find a matching task, **Then** the MCP tool returns an error and the agent translates it into a friendly message.

---

### User Story 5 - Persistent Conversation Context Across Requests (Priority: P1)

A user carries on a multi-turn conversation with the agent through the Chat API. Each request is stateless — the backend loads the full conversation history from the database, appends the new message, sends it to the Groq agent for processing, and persists the updated conversation. The agent uses this history to resolve follow-up references.

**Why this priority**: Without conversation persistence, the stateless API cannot maintain context across requests, making multi-turn interactions impossible. This is architecturally foundational.

**Independent Test**: Send a sequence of related messages to the Chat API. Verify each response correctly references prior context and all messages are persisted in order.

**Acceptance Scenarios**:

1. **Given** a user just created a task via the Chat API, **When** they send "Also mark it as important" in the next request, **Then** the agent uses conversation history to identify the recently created task and updates it.
2. **Given** a user asked "Show my tasks" and received a list, **When** they send "Complete the first one", **Then** the agent identifies the first task from the prior response and marks it complete via MCP tool.
3. **Given** the server restarts between two requests, **When** the user sends a follow-up message, **Then** the conversation context is fully available from the database and the agent responds correctly.

---

### User Story 6 - MCP Tool Response Determinism and Structured Output (Priority: P2)

Every MCP tool invocation returns a structured, deterministic response (success/failure status, affected data, error details) so the Groq agent can reliably formulate user-facing messages. MCP tools contain no conversational logic — they perform database operations and return structured results.

**Why this priority**: Structured tool responses are essential for the agent to generate accurate and consistent user-facing messages. Without this, tool output would be unpredictable.

**Independent Test**: Invoke each MCP tool directly with valid and invalid inputs. Verify all responses follow the same structured format regardless of outcome.

**Acceptance Scenarios**:

1. **Given** an MCP tool is invoked with valid parameters, **When** the operation succeeds, **Then** the tool returns a structured response containing task_id, status, and relevant data.
2. **Given** an MCP tool is invoked with invalid parameters (e.g., non-existent task ID), **When** the operation fails, **Then** the tool returns a structured error response with failure status and error description.
3. **Given** any MCP tool invocation, **When** the response is returned, **Then** it follows a consistent schema across all tools.

---

### Edge Cases

- What happens when the agent cannot understand the user's intent? It responds with a helpful message suggesting supported actions (create, view, update, delete, complete tasks).
- What happens when a user references a task that doesn't exist? The MCP tool returns a structured "not found" error, and the agent translates it into a friendly message.
- What happens when the user is not authenticated? The Chat API rejects the request with an authentication error before reaching the agent.
- What happens when an MCP tool invocation fails due to a database error? The tool returns a structured error, and the agent responds with a user-friendly message without exposing technical details.
- What happens when the user sends an empty message? The agent responds with a greeting or prompt like "How can I help you with your tasks today?"
- What happens when the user's message contains multiple intents (e.g., "Create a task and show my list")? The agent processes them through sequential MCP tool calls and responds to each.
- What happens when conversation history grows very large? The system loads a bounded window of recent messages to stay within AI model context limits.
- What happens after a server restart? All conversation state is loaded from the database — no data is lost since nothing is stored in memory.
- What happens when the MCP server is unavailable? The agent catches the connection error and returns a user-friendly message about temporary unavailability.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a Chat API endpoint that accepts natural-language messages from authenticated users and returns agent responses.
- **FR-002**: System MUST be stateless between requests — all conversation state MUST be loaded from and persisted to the database on every request.
- **FR-003**: System MUST persist every user message and agent response to the database as part of the conversation record.
- **FR-004**: System MUST load conversation history from the database and include it as context when invoking the Groq agent.
- **FR-005**: System MUST implement an MCP server using the official MCP SDK that hosts task operation tools.
- **FR-006**: System MUST use Groq SDK for AI agent — the agent discovers tools from MCP server, selects tools based on user intent, and invokes them via MCP protocol.
- **FR-007**: System MUST implement task tools following MCP specification: each tool has a name, description, parameter schema (JSON Schema), and returns structured results.
- **FR-008**: MCP tools MUST contain no conversational logic — they perform data operations and return structured responses only.
- **FR-009**: The Groq agent MUST NOT have direct database access — all data operations MUST go through MCP tools.
- **FR-010**: System MUST scope all task operations to the authenticated user — user_id MUST be explicitly provided to each MCP tool invocation.
- **FR-011**: System MUST require valid user authentication before processing any chat message.
- **FR-012**: MCP server MUST expose these tools: add_task, list_tasks, get_task, update_task, complete_task, delete_task.
- **FR-013**: Each MCP tool MUST return a structured response with consistent schema: task_id, status, and relevant data fields.
- **FR-014**: System MUST validate MCP tool inputs using parameter schemas before execution — invalid inputs return structured error responses.
- **FR-015**: System MUST handle MCP server errors and agent errors gracefully — returning user-friendly messages without exposing internal errors, stack traces, or model outputs.
- **FR-016**: System MUST survive server restarts without loss of conversation or task state.
- **FR-017**: System MUST handle requests that fall outside supported task operations by returning a helpful message listing available capabilities.
- **FR-018**: MCP server MUST be independently testable — tools can be invoked directly without going through the AI agent.

### Key Entities

- **Conversation**: A persistent record of a chat session between a user and the agent. Attributes: unique identifier, user association, creation timestamp, last activity timestamp.
- **Chat Message**: A single message within a conversation. Attributes: sender type (user or assistant), content (text), timestamp, ordering position, associated conversation.
- **MCP Tool**: A function hosted by the MCP server that performs a specific task operation. Attributes: tool name, description, parameter schema (JSON Schema), execution logic. Types: add_task, list_tasks, get_task, update_task, complete_task, delete_task.
- **Tool Response**: The structured result of an MCP tool invocation. Attributes: task_id, status (created/updated/completed/deleted/error), title, and optional error message.
- **Task** (existing entity): A user-scoped todo item. Attributes: id, user_id, title, description, completed, timestamps. Managed exclusively through MCP tools.

## MCP Tools Specification

### Tool: add_task

**Purpose**: Create a new task

**Parameters**:
- `user_id` (string, required): User identifier
- `title` (string, required): Task title
- `description` (string, optional): Task description

**Returns**:
```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

**Example Input**: `{"user_id": "user123", "title": "Buy groceries", "description": "Milk, eggs, bread"}`

---

### Tool: list_tasks

**Purpose**: Retrieve tasks from the list

**Parameters**:
- `user_id` (string, required): User identifier
- `status` (string, optional): Filter by status ("all", "pending", "completed")

**Returns**:
```json
[
  {"id": 1, "title": "Buy groceries", "completed": false},
  {"id": 2, "title": "Call mom", "completed": true}
]
```

**Example Input**: `{"user_id": "user123", "status": "pending"}`

---

### Tool: get_task

**Purpose**: Get a specific task by ID

**Parameters**:
- `user_id` (string, required): User identifier
- `task_id` (integer, required): Task identifier

**Returns**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-29T10:00:00Z"
}
```

---

### Tool: complete_task

**Purpose**: Mark a task as complete

**Parameters**:
- `user_id` (string, required): User identifier
- `task_id` (integer, required): Task identifier

**Returns**:
```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

**Example Input**: `{"user_id": "user123", "task_id": 3}`

---

### Tool: delete_task

**Purpose**: Remove a task from the list

**Parameters**:
- `user_id` (string, required): User identifier
- `task_id` (integer, required): Task identifier

**Returns**:
```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

**Example Input**: `{"user_id": "user123", "task_id": 2}`

---

### Tool: update_task

**Purpose**: Modify task title or description

**Parameters**:
- `user_id` (string, required): User identifier
- `task_id` (integer, required): Task identifier
- `title` (string, optional): New task title
- `description` (string, optional): New task description

**Returns**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

**Example Input**: `{"user_id": "user123", "task_id": 1, "title": "Buy groceries and fruits"}`

## Agent Behavior Specification

| User Says | Agent Should |
|-----------|-------------|
| "Add a task to buy groceries" | Call add_task with title "Buy groceries" |
| "Show me all my tasks" | Call list_tasks with status "all" |
| "What's pending?" | Call list_tasks with status "pending" |
| "Mark task 3 as complete" | Call complete_task with task_id 3 |
| "Delete the meeting task" | Call list_tasks first, then delete_task |
| "Change task 1 to 'Call mom tonight'" | Call update_task with new title |
| "I need to remember to pay bills" | Call add_task with title "Pay bills" |
| "What have I completed?" | Call list_tasks with status "completed" |

**Guidelines**:
- Be friendly and conversational
- Extract task details from natural language
- When users say "that task", "the first one", "it", use conversation history to identify which task they mean
- For delete operations, ALWAYS ask for confirmation before calling delete_task
- If a user's request is ambiguous, ask clarifying questions
- Format task lists in a readable way with numbers
- Never expose raw errors - translate them into friendly messages
- When showing tasks, include their status (pending/completed) and any relevant details

## Assumptions

- The existing todo/task database schema is in place and functional (tasks table with user_id foreign key, standard CRUD operations available at the database level).
- The existing authentication system (JWT-based) is in place and can provide verified user identity to the Chat API endpoint.
- Official MCP SDK (Python package `mcp`) is used to host tools as an MCP server.
- Groq SDK is used for AI agent — the agent connects to MCP server to discover and invoke tools.
- MCP server runs as part of the FastAPI application (embedded, not a separate process) for simplicity.
- User context (user_id) is passed to MCP tools via tool parameters.
- A single active conversation per user is sufficient for the initial implementation.
- Conversation history sent to the AI model is bounded by a reasonable message window to stay within context limits (assumption: last 50 messages or configurable).
- The Chat API is a synchronous request/response endpoint (no streaming in initial implementation).
- MCP tools are implemented as Python functions, registered with MCP server using official MCP SDK decorators or registration methods.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can manage tasks (create, view, update, complete, delete) entirely through natural-language chat messages without using any other interface.
- **SC-002**: Conversation context persists across multiple stateless API requests — users can make follow-up references spanning at least 5 consecutive messages.
- **SC-003**: The system operates correctly after a server restart with zero loss of conversation history or task data.
- **SC-004**: All task mutations flow exclusively through MCP tool invocations — zero direct database access from the AI agent layer.
- **SC-005**: All MCP tool responses follow a consistent structured schema, enabling the agent to reliably interpret results.
- **SC-006**: All error scenarios result in user-friendly messages — zero raw error traces or technical internals exposed to users.
- **SC-007**: No user can access, view, or modify another user's tasks through the chat agent under any circumstances.
- **SC-008**: The agent correctly identifies user intent and selects appropriate MCP tools for standard task operations at least 90% of the time.
- **SC-009**: MCP tools can be tested independently from the agent — direct tool invocation returns expected structured responses.
- **SC-010**: The MCP server successfully registers all required tools and makes them discoverable to the Groq agent.

## Conversation Flow (Stateless Request Cycle)

1. Receive user message at Chat API endpoint
2. Validate JWT authentication and extract user_id
3. Fetch conversation history from database
4. Build message array for agent (history + new message)
5. Store user message in database
6. Initialize Groq agent with MCP server connection
7. Agent discovers available MCP tools from server
8. Run agent with conversation context
9. Agent invokes appropriate MCP tool(s) via MCP protocol
10. MCP server executes tool, performs database operation
11. MCP server returns structured response to agent
12. Agent formulates user-friendly response
13. Store assistant response in database
14. Return response to client
15. Server holds NO state (ready for next request)

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Next.js with ChatKit-style UI |
| Backend | Python FastAPI |
| AI Framework | Groq SDK |
| MCP Server | Official MCP SDK (Python) |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (JWT) |

## Out of Scope

- Streaming responses (future enhancement)
- Multiple concurrent conversations per user
- Voice input/output
- Task attachments or file uploads
- Task sharing between users
- Advanced task filtering (tags, categories, priorities)
- Task reminders or notifications
- OpenAI Agents SDK (using Groq instead)
- Separate MCP server process (embedded in FastAPI)

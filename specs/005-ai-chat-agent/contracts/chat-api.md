# API Contracts: Chat Endpoints

**Feature**: 005-ai-chat-agent | **Date**: 2026-01-29 | **Updated**: Spec-6/7 alignment

## POST /api/chat

Send a user message and receive an agent response.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body**:
```json
{
  "message": "Add a task to buy groceries by Friday",
  "conversation_id": "uuid-optional"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message | string | yes | User's natural language message (1-2000 chars) |
| conversation_id | UUID | no | Existing conversation ID. If omitted, uses or creates the user's active conversation |

### Response (200 OK)

```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "role": "assistant",
    "content": "Done! I've created a task 'Buy groceries' due this Friday.",
    "tool_calls": [
      {
        "tool": "add_task",
        "input": {"title": "Buy groceries"},
        "result": {"status": "success", "data": {"id": "...", "title": "Buy groceries", "completed": false}}
      }
    ],
    "created_at": "2026-01-29T10:30:00Z"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| conversation_id | UUID | The conversation this message belongs to |
| message.id | UUID | Unique message identifier |
| message.role | string | Always "assistant" for responses |
| message.content | string | Agent's natural language response |
| message.tool_calls | array\|null | Tools invoked during response (for transparency) |
| message.created_at | datetime | Message timestamp |

### Error Responses

**401 Unauthorized** — Missing or invalid JWT token
```json
{
  "detail": "Invalid token",
  "error_code": "UNAUTHORIZED",
  "status_code": 401
}
```

**422 Validation Error** — Invalid request body
```json
{
  "detail": "Message cannot be empty",
  "error_code": "VALIDATION_ERROR",
  "status_code": 422
}
```

**500 Internal Server Error** — Agent or system failure
```json
{
  "detail": "I'm having trouble processing your request. Please try again.",
  "error_code": "INTERNAL_ERROR",
  "status_code": 500
}
```

---

## GET /api/chat/history

Retrieve conversation history for the authenticated user.

### Request

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| conversation_id | UUID | no | active conversation | Specific conversation to load |
| limit | int | no | 50 | Max messages to return (1-100) |
| before | UUID | no | null | Cursor: return messages before this message ID (for pagination) |

### Response (200 OK)

```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "role": "user",
      "content": "Show me my tasks",
      "tool_calls": null,
      "created_at": "2026-01-29T10:25:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "role": "assistant",
      "content": "Here are your current tasks:\n\n1. Buy groceries (pending)\n2. Prepare presentation (completed)",
      "tool_calls": [
        {
          "tool": "list_tasks",
          "input": {},
          "result": {"status": "success", "data": {"tasks": [...], "count": 2}}
        }
      ],
      "created_at": "2026-01-29T10:25:02Z"
    }
  ],
  "has_more": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| conversation_id | UUID | The conversation these messages belong to |
| messages | array | Ordered list of messages (oldest first) |
| has_more | boolean | Whether more messages exist before the returned set |

### Error Responses

**401 Unauthorized** — Missing or invalid JWT token

**404 Not Found** — No conversation found for user (return empty state)
```json
{
  "conversation_id": null,
  "messages": [],
  "has_more": false
}
```

---

## Tool Schemas (MCP-Compatible via Groq)

All tools follow a consistent schema pattern for Groq tool calling.

### Groq Tool Definition Format

```json
{
  "type": "function",
  "function": {
    "name": "tool_name",
    "description": "Clear description for the AI agent",
    "parameters": {
      "type": "object",
      "properties": { ... },
      "required": [...]
    }
  }
}
```

### Tool Response Schema (Consistent for all tools)

```json
{
  "status": "success" | "error",
  "data": { ... } | null,
  "error": { "type": "string", "message": "string" } | null
}
```

---

### add_task

**Description**: Create a new task for the user

**Input**:
```json
{
  "title": "Buy groceries",
  "description": "Get milk, eggs, and bread"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | yes | Task title (1-500 chars) |
| description | string | no | Task description (max 5000 chars) |

**Note**: `user_id` is injected server-side from JWT, not provided by agent.

**Output (success)**:
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "title": "Buy groceries",
    "description": "Get milk, eggs, and bread",
    "completed": false,
    "created_at": "2026-01-29T10:30:00Z"
  }
}
```

**Output (error)**:
```json
{
  "status": "error",
  "error": {
    "type": "validation_error",
    "message": "Title is required"
  }
}
```

---

### list_tasks

**Description**: List all tasks for the user, optionally filtered by status

**Input**:
```json
{
  "status": "pending",
  "limit": 20
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | no | Filter: "pending", "completed", or "all" (default: "all") |
| limit | int | no | Max results (default: 20) |

**Output (success)**:
```json
{
  "status": "success",
  "data": {
    "tasks": [
      {"id": "uuid", "title": "Buy groceries", "completed": false, "created_at": "..."},
      {"id": "uuid", "title": "Prepare presentation", "completed": true, "created_at": "..."}
    ],
    "count": 2
  }
}
```

**Output (empty)**:
```json
{
  "status": "success",
  "data": {
    "tasks": [],
    "count": 0
  }
}
```

---

### update_task

**Description**: Update an existing task's title, description, or completion status

**Input**:
```json
{
  "task_id": "uuid",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| task_id | string | yes | Task to update |
| title | string | no | New title |
| description | string | no | New description |
| completed | boolean | no | New completion status |

**Output (success)**:
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "title": "Updated title",
    "description": "Updated description",
    "completed": true,
    "updated_at": "2026-01-29T10:35:00Z"
  }
}
```

**Output (error - not found)**:
```json
{
  "status": "error",
  "error": {
    "type": "not_found",
    "message": "Task not found"
  }
}
```

---

### complete_task

**Description**: Mark a task as completed

**Input**:
```json
{
  "task_id": "uuid"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| task_id | string | yes | Task to complete |

**Output (success)**:
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "title": "Buy groceries",
    "completed": true,
    "completed_at": "2026-01-29T10:40:00Z"
  }
}
```

---

### delete_task

**Description**: Delete a task permanently

**Input**:
```json
{
  "task_id": "uuid"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| task_id | string | yes | Task to delete |

**Output (success)**:
```json
{
  "status": "success",
  "data": {
    "deleted": true,
    "task_id": "uuid"
  }
}
```

**Output (error - not found)**:
```json
{
  "status": "error",
  "error": {
    "type": "not_found",
    "message": "Task not found"
  }
}
```

---

## Security Notes

1. **User ID Injection**: `user_id` is NEVER accepted from the agent's tool call arguments. It is always injected server-side from the validated JWT token.

2. **Ownership Validation**: Every tool validates that the task belongs to the authenticated user before performing any operation.

3. **No Internal Leakage**: Error responses never include stack traces, internal IDs, or system details beyond the structured error type and message.

# Research: AI Chat Agent with Groq Tool Calling

**Feature**: 005-ai-chat-agent | **Date**: 2026-01-29 | **Updated**: Spec-6/7 alignment

## Research Topics

### 1. Groq SDK Integration with FastAPI

**Decision**: Use `groq` Python SDK for tool calling. Implement MCP-compatible tool design using Groq's native function/tool calling interface.

**Rationale**:
- Groq provides fast inference with tool/function calling support
- Groq's tool calling interface is compatible with MCP tool schema design (name, description, parameters)
- The spec explicitly requires "Groq SDK used for tool calling (not official MCP SDK)"
- Groq API is OpenAI-compatible, simplifying migration if needed later

**Alternatives Considered**:
- **OpenAI Agents SDK**: Would work but user spec explicitly requires Groq SDK
- **Official MCP Runtime**: Spec explicitly excludes this ("Not Building: Official MCP server/runtime integration")
- **LangChain**: Heavier framework, adds unnecessary abstraction

**Integration Pattern**:
```python
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Tool definitions follow MCP-compatible schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                },
                "required": ["title"]
            }
        }
    },
    # ... more tools
]

# Per-request agent execution
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=conversation_history,
    tools=tools,
    tool_choice="auto"
)
```

### 2. MCP-Compatible Tool Architecture (via Groq)

**Decision**: Implement tools as Python functions with Pydantic schemas. Register tools with Groq's tool calling interface using JSON Schema definitions. Tools wrap existing `task_service.py` functions.

**Rationale**:
- MCP-compatible design: each tool has name, description, parameter schema, returns structured results
- Tools are thin adapters over existing database service layer
- Pydantic ensures validation at tool input/output boundaries
- Tools contain NO conversational logic (per spec requirement)
- Agent has NO direct database access (all through tools)

**Alternatives Considered**:
- **Official MCP SDK with MCP server**: Spec explicitly excludes this
- **Raw function calls without schema**: Would bypass validation and MCP-compatible design

**Tool List** (maps to spec FR-011):

| Tool | Purpose | Service Function |
|------|---------|------------------|
| `add_task` | Create a new task | `task_service.create_task` |
| `list_tasks` | List user's tasks with filters | `task_service.get_user_tasks` |
| `update_task` | Update task fields | `task_service.update_task` |
| `complete_task` | Mark task as complete | `task_service.toggle_task_completion` |
| `delete_task` | Delete a task | `task_service.delete_task` |

### 3. Tool Response Schema (FR-012)

**Decision**: All tools return a consistent structured response with `status`, `data`, and `error` fields.

**Schema**:
```python
class ToolResponse(BaseModel):
    status: Literal["success", "error"]
    data: Optional[dict] = None  # Entity or result set
    error: Optional[dict] = None  # {"type": str, "message": str}

# Success example
{"status": "success", "data": {"id": "...", "title": "Buy groceries", "completed": false}}

# Error example
{"status": "error", "error": {"type": "not_found", "message": "Task not found"}}
```

**Rationale**:
- Consistent schema enables agent to reliably interpret results (SC-005)
- Separates success/error paths clearly
- No conversational text in tool responses (FR-007)
- No stack traces or internal details (FR-013)

### 4. Stateless Architecture with Database Persistence

**Decision**: Backend is completely stateless. All conversation context stored in PostgreSQL. Rebuilt from database on every request.

**Flow per request**:
1. Authenticate user (JWT validation)
2. Load conversation history from database (or create new conversation)
3. Append new user message to database
4. Build prompt: system prompt + history + user input
5. Execute Groq completion with tools
6. If tool call: execute tool, get result, continue completion
7. Store assistant response (with tool_calls if any) to database
8. Return response to client

**Rationale**:
- Satisfies FR-002 (stateless between requests)
- Satisfies FR-014 (survives server restarts)
- Satisfies constitution "Stateless Architecture Mandate"

**Message Window**: Load last 50 messages (configurable) to stay within model context limits.

### 5. Tool Execution Loop

**Decision**: Implement iterative tool execution loop that handles Groq's tool call responses.

**Pattern**:
```python
async def execute_agent(messages: list[dict], user_id: str) -> AgentResult:
    while True:
        response = await groq_client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto"
        )

        choice = response.choices[0]

        # If no tool calls, we have the final response
        if not choice.message.tool_calls:
            return AgentResult(
                content=choice.message.content,
                tool_calls=collected_tool_calls
            )

        # Execute each tool call
        for tool_call in choice.message.tool_calls:
            result = await execute_tool(
                name=tool_call.function.name,
                arguments=json.loads(tool_call.function.arguments),
                user_id=user_id
            )
            # Add tool result to messages for next iteration
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Add assistant's tool call message
        messages.append(choice.message)
```

### 6. Authentication Flow for Chat

**Decision**: Reuse existing JWT authentication. Pass extracted `user_id` to all tool invocations as a fixed parameter (not user-controllable).

**Security Flow**:
- `POST /api/chat` uses `Depends(get_current_user_id)`
- `user_id` is injected into every tool call automatically
- Tools validate user ownership for all data operations
- Agent prompt NEVER includes user_id instructions (prevents prompt injection)

### 7. Environment Variables

**Decision**: Add Groq-specific configuration to existing `.env`.

| Variable | Purpose | Default |
|----------|---------|---------|
| `GROQ_API_KEY` | Groq API authentication | (required) |
| `GROQ_MODEL` | Model for tool calling | `llama-3.3-70b-versatile` |
| `CHAT_CONTEXT_MESSAGES` | Number of history messages for context | `50` |

### 8. Error Handling Strategy

**Decision**: Wrap all tool failures in structured responses. Agent translates to conversational messages.

**Error Flow**:
```
Tool raises exception / returns error
  → Caught and wrapped in ToolResponse(status="error", error={...})
  → Agent receives structured error
  → Agent generates: "I couldn't find that task. Could you describe it differently?"
  → User sees conversational error, not technical details
```

**Error Types**:
- `not_found`: Task doesn't exist or not owned by user
- `validation_error`: Invalid input parameters
- `unauthorized`: User doesn't own the resource
- `internal_error`: Database or system failure (logged, not exposed)

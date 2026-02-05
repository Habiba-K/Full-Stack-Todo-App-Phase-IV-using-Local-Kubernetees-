# Data Model: AI Chat Agent & Conversation Orchestration

**Feature**: 005-ai-chat-agent | **Date**: 2026-01-27

## Existing Entities (unchanged)

### User
Already defined in `backend/src/models/user.py`.

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, default uuid4 |
| email | string(255) | unique, indexed, not null |
| password_hash | string(255) | not null |
| name | string(100) | nullable |
| created_at | datetime | default utcnow |
| updated_at | datetime | default utcnow |

### Task
Already defined in `backend/src/models/task.py`.

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, default uuid4 |
| user_id | string(255) | indexed, not null |
| title | string(500) | not null |
| description | text | nullable |
| completed | boolean | default false |
| created_at | datetime | default utcnow |
| updated_at | datetime | default utcnow |

## New Entities

### Conversation
Represents a chat session between a user and the AI agent.

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, default uuid4 |
| user_id | UUID | FK → users.id, indexed, not null |
| title | string(255) | nullable, auto-generated from first message |
| created_at | datetime | default utcnow |
| updated_at | datetime | default utcnow |

**Relationships**:
- Belongs to one User (many-to-one)
- Has many Messages (one-to-many, ordered by created_at)

**Business Rules**:
- One active conversation per user (initial implementation)
- If no conversation exists for a user, create one on first chat message
- `updated_at` is set whenever a new message is added
- `title` is auto-set from the first user message (truncated to 100 chars)

### Message
Represents a single message in a conversation (user or assistant).

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, default uuid4 |
| conversation_id | UUID | FK → conversations.id, indexed, not null |
| role | string(20) | enum: "user", "assistant", not null |
| content | text | not null |
| tool_calls | JSON | nullable, stores MCP tool invocations for assistant messages |
| created_at | datetime | default utcnow |

**Relationships**:
- Belongs to one Conversation (many-to-one)

**Business Rules**:
- Messages are immutable — once created, never updated or deleted
- Messages are always ordered by `created_at` ascending
- `role` is either "user" (human input) or "assistant" (agent response)
- `tool_calls` stores a JSON array of tool invocations made during the assistant's response (for debugging/auditing)
- Messages are retrieved in bulk (last N) for agent context

## Entity Relationship Diagram

```
┌──────────┐       ┌───────────────┐       ┌──────────┐
│  users   │──1:N──│ conversations │──1:N──│ messages │
│          │       │               │       │          │
│ id (PK)  │       │ id (PK)       │       │ id (PK)  │
│ email    │       │ user_id (FK)  │       │ conv_id  │
│ ...      │       │ title         │       │ role     │
└──────────┘       │ created_at    │       │ content  │
      │            │ updated_at    │       │ tool_calls│
      │            └───────────────┘       │ created_at│
      │                                    └──────────┘
      │
      │            ┌──────────┐
      └────1:N─────│  tasks   │
                   │          │
                   │ id (PK)  │
                   │ user_id  │
                   │ title    │
                   │ ...      │
                   └──────────┘
```

## Indexes

| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| conversations | ix_conversations_user_id | user_id | Look up user's conversation |
| messages | ix_messages_conversation_id | conversation_id | Load messages for a conversation |
| messages | ix_messages_created_at | conversation_id, created_at | Efficiently load recent messages |

## State Transitions

### Conversation Lifecycle
```
[No Conversation] → (first chat message) → [Active]
[Active] → (messages added) → [Active]
```

### Message Lifecycle
```
[Created] → (immutable, no transitions)
```

## Validation Rules

- `conversation.user_id` must reference a valid user
- `message.conversation_id` must reference a valid conversation
- `message.role` must be "user" or "assistant"
- `message.content` must not be empty
- `message.tool_calls` must be valid JSON array or null

---
id: 016
title: AI Chat Agent Groq Implementation Planning
stage: plan
date: 2026-01-29
surface: agent
model: claude-opus-4-5
feature: 005-ai-chat-agent
branch: 005-ai-chat-agent
user: user
command: /sp.plan
labels: ["plan", "groq", "tool-calling", "stateless", "chat-api"]
links:
  spec: specs/005-ai-chat-agent/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-ai-chat-agent/plan.md (updated)
  - specs/005-ai-chat-agent/research.md (updated)
  - specs/005-ai-chat-agent/quickstart.md (updated)
  - specs/005-ai-chat-agent/contracts/chat-api.md (updated)
  - specs/005-ai-chat-agent/data-model.md (unchanged)
  - CLAUDE.md (updated by script)
tests:
  - N/A (planning phase)
---

## Prompt

Spec-6/7

1. Define database models:
   - Task (user_id, title, description, completed, timestamps)
   - Conversation (user_id, created_at, updated_at)
   - Message (conversation_id, role, content, timestamp)

2. Implement stateless Chat API endpoint:
   - POST /api/{user_id}/chat
   - Accepts conversation_id (optional) and message

3. On each chat request:
   - Authenticate user
   - Fetch conversation history from database
   - Append new user message
   - Build prompt (system + history + user input)

4. Execute AI agent:
   - Use Groq SDK with tool definitions
   - Provide tool schemas (JSON / Pydantic)
   - Allow agent to choose appropriate tool

5. Tool execution layer:
   - add_task
   - list_tasks
   - update_task
   - complete_task
   - delete_task

6. Tool behavior rules:
   - Each tool performs exactly one task operation
   - Validate inputs using Pydantic schemas
   - Enforce user-level task ownership
   - Persist changes using SQLModel
   - Return structured JSON responses

7. Error handling:
   - Task not found
   - Invalid input
   - Unauthorized access
   - Tool execution failures

8. Persistence:
   - Store user messages before agent execution
   - Store assistant responses after execution
   - Store tool calls and results (if any)

9. Response to client:
   - conversation_id
   - assistant response
   - list of invoked tools (if applicable)

10. Ensure system guarantees:
    - Stateless server operation
    - Conversation resume after refresh/restart
    - Deterministic tool behavior
    - Friendly confirmations and clear errors

11. Testing & validation:
    - Manual API testing for all tool paths
    - Conversation continuity verification
    - Task ownership and validation checks

## Response snapshot

Updated planning artifacts for Spec-6/7 alignment with Groq SDK (replacing OpenAI Agents SDK):

**Key Changes:**
- Updated research.md with Groq SDK integration patterns
- Updated plan.md with 6-phase implementation (DB → Tools → Agent → API → Frontend → Testing)
- Updated quickstart.md with Groq environment variables and setup
- Updated contracts/chat-api.md with MCP-compatible tool schemas via Groq

**Architecture:**
- Groq SDK for AI tool calling (not official MCP SDK per spec requirement)
- MCP-compatible tool design (name, description, parameters, structured responses)
- Stateless backend - conversation rebuilt from PostgreSQL on every request
- Tools wrap existing task_service.py - agent has no direct DB access

**Implementation Phases:**
1. Database Models (Conversation, Message)
2. Tool Layer (Pydantic schemas, task tools)
3. Agent Service (Groq integration, tool execution loop)
4. Chat API Endpoints (POST /api/chat, GET /api/chat/history)
5. Frontend Chat UI (Next.js components)
6. Testing & Validation

**Constitution Check:** PASS with documented MCP adaptation

## Outcome

- ✅ Impact: Complete implementation plan for Groq-based chat agent
- 🧪 Tests: N/A (planning phase)
- 📁 Files: 4 files updated (plan.md, research.md, quickstart.md, chat-api.md)
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks
- 🧠 Reflection: Spec-6/7 explicitly requires Groq SDK, not OpenAI - updated all artifacts

## Evaluation notes (flywheel)

- Failure modes observed: None - spec requirements were clear
- Graders run and results (PASS/FAIL): Constitution check PASS (with MCP adaptation)
- Prompt variant (if applicable): User provided detailed 11-point implementation outline
- Next experiment (smallest change to try): Proceed to task breakdown with /sp.tasks

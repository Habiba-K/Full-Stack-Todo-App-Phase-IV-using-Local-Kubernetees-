---
id: 003
title: Phase-III AI Chatbot Constitution
stage: constitution
date: 2026-01-27
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 003-ui-homepage
user: user
command: /sp.constitution
labels: ["constitution", "phase-iii", "ai-chatbot", "mcp", "stateless", "openai-agents"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
Project: Phase-III – AI Todo Chatbot (MCP + OpenAI Agents)

Core principles:
- Stateless backend architecture
- Agent-driven task management
- MCP tool–only data mutations
- Database as single source of truth
- Clear separation of Agent, MCP, API, and UI

Key standards:
- All task operations MUST go through MCP tools
- AI agents MUST NOT access the database directly
- Conversation context rebuilt from DB every request
- FastAPI server holds NO in-memory state
- All actions confirmed in natural language

Technology constraints:
- Frontend: OpenAI ChatKit
- Backend: FastAPI (Python)
- AI: OpenAI Agents SDK
- MCP: Official MCP SDK
- Database: Neon PostgreSQL
- Auth: Better Auth

Security rules:
- JWT-based user authentication required
- All data scoped strictly to authenticated user
- Cross-user access prohibited

Constraints:
- No hard-coded task logic outside MCP tools
- No server-side session state
- No UI logic in backend or agent

Success criteria:
- Users manage todos via natural language
- Agent selects correct MCP tools consistently
- Conversation persists across requests and restarts
- System passes statelessness and auth checks
```

## Response snapshot

Updated constitution from version 1.0.0 to 2.0.0 (MAJOR version bump) to reflect the architectural shift from traditional web application to AI-driven chatbot system.

**Key Changes:**
- Redefined all 7 core principles for stateless, agent-driven architecture
- Added Stateless Architecture Mandate as Principle II
- Replaced Clean Architecture with Agent/MCP/API/UI separation model
- Added MCP Tool-Only Data Access as Principle IV
- Added Conversation-Driven Design as Principle V
- Added Database as Single Source of Truth as Principle VI
- Updated Security-First Design for agent-based auth and prompt injection prevention

**Technology Stack Changes:**
- Frontend: Next.js → OpenAI ChatKit
- Added: OpenAI Agents SDK for AI orchestration
- Added: MCP SDK for tool definitions
- Removed: Traditional REST API patterns
- Added: Conversation persistence requirements

**New Requirements:**
- MCP tools: create_todo, list_todos, get_todo, update_todo, delete_todo, complete_todo, incomplete_todo
- API endpoints: POST /api/chat, GET /api/chat/history
- Database schema: Added conversations and messages tables
- Agent behavior standards: No hallucination, conversational responses, tool selection validation

**Removed Requirements:**
- Traditional CRUD UI pages
- Direct frontend-to-database patterns
- Server-side session management

## Outcome

- ✅ Impact: Major architectural redefinition - backward incompatible with Phase-II web application approach
- 🧪 Tests: No tests modified (constitution document only)
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Update plan-template.md, spec-template.md, and tasks-template.md to align with Phase-III principles
- 🧠 Reflection: This constitution establishes the foundation for AI-first development with strict separation between agent reasoning and data operations through MCP tools. The stateless architecture mandate is critical for production scalability.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution successfully updated with comprehensive Phase-III principles
- Graders run and results (PASS/FAIL): Manual review - PASS (all placeholders filled, version incremented correctly, sync impact documented)
- Prompt variant (if applicable): Standard /sp.constitution command
- Next experiment (smallest change to try): Apply constitution principles to first Phase-III feature specification to validate conversational user story format

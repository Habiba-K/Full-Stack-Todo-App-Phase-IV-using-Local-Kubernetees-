---
id: 002
title: Phase-III Constitution Update
stage: constitution
date: 2026-01-27
surface: agent
model: claude-opus-4-5
feature: none
branch: 003-ui-homepage
user: user
command: /sp.constitution
labels: ["constitution", "governance", "principles", "mcp", "agent", "stateless", "phase-iii"]
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

/sp.constitution

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

## Response snapshot

Updated constitution from v1.0.0 (Phase-II: Todo Full-Stack Web App) to v2.0.0 (Phase-III: AI Todo Chatbot). This is a MAJOR version bump due to backward-incompatible redefinition of all principles, architecture, and technology stack.

**Core Principles (7 total, redefined)**:
1. Security-First Design — updated for MCP/agent context, user scoping at tool level
2. Stateless Backend Architecture — NEW: no in-memory state, DB-rebuilt context
3. Agent-Driven Task Management — NEW: agent as intelligent router, MCP-only tool invocation
4. MCP Tool-Only Data Mutations — NEW: exclusive mutation interface
5. Database as Single Source of Truth — NEW: all state in Neon PostgreSQL
6. Clean Architecture — Layer Separation — redefined for 4-layer model (UI/API/Agent/MCP)
7. Natural Language Confirmation — NEW: all actions confirmed in chat

**Technology Stack Changes**:
- Frontend: Next.js → OpenAI ChatKit
- AI Layer: None → OpenAI Agents SDK
- Tool Protocol: None → Official MCP SDK
- ORM: SQLModel → async database drivers (asyncpg)

**Template Consistency**:
- plan-template.md: Compatible (generic Constitution Check)
- spec-template.md: Compatible (generic user story format)
- tasks-template.md: Compatible (generic phase structure)

**Version**: 2.0.0 | Ratified: 2026-01-22 | Last Amended: 2026-01-27

## Outcome

- ✅ Impact: Complete constitution redefinition for Phase-III AI Todo Chatbot with MCP + OpenAI Agents architecture
- 🧪 Tests: None (documentation artifact)
- 📁 Files: Updated .specify/memory/constitution.md (291 lines, v1.0.0 → v2.0.0)
- 🔁 Next prompts: Ready for /sp.specify to create Phase-III feature specifications following new constitution
- 🧠 Reflection: Major version bump justified — every principle was either redefined or replaced. The 4-layer architecture (UI/API/Agent/MCP) and MCP-only mutation principle are the most significant structural changes from Phase-II's 3-layer web app model.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (constitution update)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate new principles during first Phase-III feature specification

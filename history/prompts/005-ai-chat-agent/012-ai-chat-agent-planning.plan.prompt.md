---
id: 012
title: AI Chat Agent Implementation Planning
stage: plan
date: 2026-01-27
surface: agent
model: claude-opus-4-5-20251101
feature: 005-ai-chat-agent
branch: 005-ai-chat-agent
user: user
command: /sp.plan
labels: ["ai-agent", "chat", "mcp", "architecture", "fastapi", "chatkit", "openai-agents-sdk"]
links:
  spec: specs/005-ai-chat-agent/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-ai-chat-agent/plan.md
  - specs/005-ai-chat-agent/research.md
  - specs/005-ai-chat-agent/data-model.md
  - specs/005-ai-chat-agent/quickstart.md
  - specs/005-ai-chat-agent/contracts/chat-api.md
tests:
  - none
---

## Prompt

before planning first you can review the frontend and backend folder after that generate plan, here is plan:  /sp.plan Spec-5

1. Build ChatKit-based chat UI on frontend
2. Send user messages from ChatKit to FastAPI chat endpoint
3. Authenticate requests using Better Auth JWT
4. Fetch conversation history from database
5. Append new user message to agent context
6. Run OpenAI Agent via Agents SDK
7. Agent selects and invokes MCP tools
8. MCP tools perform task operations in database
9. Store assistant response and tool calls
10. Return response to ChatKit UI
11. Display confirmations and errors in chat
12. Support conversation resume after refresh

## Response snapshot

Completed full Phase 0 + Phase 1 planning for the AI Chat Agent feature. Reviewed the entire codebase (frontend: Next.js 16 with App Router, Tailwind, auth via localStorage/JWT, api-client.ts helper; backend: FastAPI with SQLModel, async Neon PostgreSQL, JWT auth via get_current_user_id dependency, task CRUD via task_service.py). Generated 5 artifacts:

1. **plan.md**: Full implementation plan with request flow architecture (ChatKit UI → POST /api/chat → JWT verify → load history → build agent context → run OpenAI Agent → MCP tools → persist response → return). Constitution check passed all 7 gates. Source code structure maps new files (models, routers, services, mcp/) to existing patterns.

2. **research.md**: 7 research decisions — OpenAI Agents SDK integration pattern (agent-per-request), MCP tool architecture (thin wrappers over task_service.py), ChatKit frontend integration, conversation persistence strategy (1 conversation/user, 20-message context), auth flow reuse, error handling in agent context, new environment variables (OPENAI_API_KEY, OPENAI_MODEL, CHAT_CONTEXT_MESSAGES).

3. **data-model.md**: 2 new entities (Conversation, Message) with full schemas, relationships, indexes, and business rules. Messages are immutable. Conversations are one-per-user initially.

4. **contracts/chat-api.md**: Full API contracts for POST /api/chat and GET /api/chat/history, plus all 7 MCP tool schemas (create_todo, list_todos, get_todo, update_todo, delete_todo, complete_todo, incomplete_todo).

5. **quickstart.md**: Setup guide with env vars, dependencies, running instructions, and test conversation examples.

## Outcome

- Impact: Complete architectural plan for AI chat agent feature, extending existing codebase with MCP tools, agent orchestration, and ChatKit frontend
- Tests: none (planning phase)
- Files: 5 new plan artifacts created
- Next prompts: /sp.tasks to generate task breakdown, then /sp.implement
- Reflection: Thorough codebase review before planning ensured accurate mapping of new components to existing patterns. The user's 12-step flow aligned perfectly with the stateless architecture mandated by the constitution.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Constitution check PASS (7/7 gates)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none

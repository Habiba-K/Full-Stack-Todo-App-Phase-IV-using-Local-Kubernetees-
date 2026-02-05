---
id: 002
title: auth-jwt-security-plan
stage: plan
date: 2026-01-22
surface: agent
model: claude-sonnet-4-5
feature: 001-auth-jwt-security
branch: 001-auth-jwt-security
user: habiba
command: /sp.plan
labels: ["authentication", "jwt", "planning", "architecture", "better-auth", "fastapi"]
links:
  spec: specs/001-auth-jwt-security/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-auth-jwt-security/plan.md
  - specs/001-auth-jwt-security/research.md
  - specs/001-auth-jwt-security/data-model.md
  - specs/001-auth-jwt-security/quickstart.md
  - specs/001-auth-jwt-security/contracts/auth-signup.yaml
  - specs/001-auth-jwt-security/contracts/auth-signin.yaml
  - specs/001-auth-jwt-security/contracts/auth-logout.yaml
  - specs/001-auth-jwt-security/contracts/auth-me.yaml
tests:
  - Constitution Check validation (6/6 gates passed)
  - Technical context completeness verified
---

## Prompt

SPEC 2 — Authentication + JWT Security (Better Auth + Next.js + FastAPI Verification)

Deliverable: Secure multi-user authentication system using Better Auth-issued JWTs verified by FastAPI, enforcing strict user isolation for all task API operations.

Plan:
1) Define Authentication Model and Token Flow
- Frontend handles signup/signin via Better Auth
- On successful login, Better Auth issues a JWT access token
- Frontend stores session using Better Auth mechanisms
- Every API call to FastAPI includes:
  - Authorization: Bearer <JWT>

2) Configure Better Auth (Next.js)
- Install Better Auth and configure providers for email/password signup/signin
- Enable JWT issuing mechanism (plugin/config required by Better Auth)
- Ensure token payload contains a stable user identifier:
  - user_id preferred
  - email acceptable as secondary identifier
- Confirm token expiry behavior (e.g., 7 days) aligns with requirements

3) Share Secret Across Frontend and Backend
- Add BETTER_AUTH_SECRET to frontend environment
- Add BETTER_AUTH_SECRET to backend environment
- Confirm both services read the same exact value
- Ensure secret is never hardcoded in source code

4) Frontend API Client Adds Token Automatically
- Build a centralized API client utility:
  - fetch wrapper or axios-based client
  - attaches Authorization header
- Ensure token is included for ALL task-related API calls
- Handle auth errors:
  - 401 should trigger re-login or session refresh behavior (simple redirect acceptable)

5) Implement JWT Verification in FastAPI
- Create auth dependency or middleware:
  - read Authorization header
  - validate Bearer format
  - verify signature using BETTER_AUTH_SECRET
  - decode payload and extract authenticated user identifier
- Reject invalid cases:
  - missing header → 401
  - malformed token → 401
  - signature failure → 401
  - expired token → 401

6) Enforce User Matching and Ownership Rules
- For every route with {user_id}:
  - compare {user_id} path param to authenticated user id from JWT
  - mismatch → 403 Forbidden
- Ensure database filtering remains enforced:
  - queries must always filter tasks by authenticated user id
  - never allow selecting tasks by id alone without user scope

7) Apply Auth Enforcement Across All Endpoints
- Require JWT for:
  - GET /api/{user_id}/tasks
  - POST /api/{user_id}/tasks
  - GET /api/{user_id}/tasks/{id}
  - PUT /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH /api/{user_id}/tasks/{id}/complete
- Ensure consistent error payload format for auth failures

8) Validation and Security Test Checklist
- No token → 401 on all endpoints
- Invalid token → 401
- Expired token → 401
- Token for user A requesting /api/userB/tasks → 403
- Token for user A can create/list/update/delete only user A tasks
- Attempt cross-user task id access blocked (403 or 404 depending on policy, but must never return data)

9) Documentation for Hackathon Submission
- Add README section:
  - auth flow diagram (steps)
  - how JWT is passed from frontend to backend
  - environment variables required
  - expected responses for 401 and 403 scenarios

## Response snapshot

Created comprehensive implementation plan for Authentication + JWT Security feature with complete Phase 0 (Research) and Phase 1 (Design & Contracts) artifacts.

**Plan Structure:**
- Technical context defined with all dependencies and constraints
- Constitution Check completed: 6/6 gates passed (Security-First, Correctness, Clean Architecture, Maintainability, Modern Standards, TDD conditional)
- Project structure documented for web application (frontend + backend)
- No complexity violations - all principles satisfied

**Phase 0 - Research (research.md):**
- 5 research tasks completed with decisions:
  1. Better Auth JWT Configuration → Default JWT with httpOnly cookie
  2. FastAPI JWT Verification → PyJWT library selected
  3. Shared Secret Management → Environment variables with validation
  4. Token Transport → Authorization Bearer header with Better Auth session
  5. Error Response Standardization → Standardized JSON format with error codes

**Phase 1 - Design & Contracts:**
- Data model (data-model.md): User entity, JWT payload structure, relationships, validation rules
- API contracts (4 OpenAPI specs): signup, signin, logout, me endpoints
- Quickstart guide (quickstart.md): Complete setup instructions with troubleshooting

**Architectural Decisions:**
- JWT Library: PyJWT (lightweight, focused)
- Token Storage: Better Auth session management (secure by default)
- Ownership Validation: FastAPI dependency with path parameter validation
- Error Format: Standardized JSON with error_code field

**Security Considerations:**
- Token security, signature verification, ownership enforcement, error handling all documented
- Production deployment checklist included
- Testing strategy defined (unit, integration, security tests)

## Outcome

- ✅ Impact: Complete architectural plan with research, design, and contracts ready for task breakdown
- 🧪 Tests: Constitution Check passed (6/6 gates), security considerations validated
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and 4 API contract specs
- 🔁 Next prompts: Run `/sp.tasks` to generate task breakdown, then `/sp.implement` to execute via specialized agents
- 🧠 Reflection: Plan successfully addresses all specification requirements with clear architectural decisions. Research phase resolved all technical unknowns. Design phase produced complete data model and API contracts. Ready for task breakdown and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all artifacts
- Graders run and results (PASS/FAIL): Constitution Check PASS (6/6 gates), Technical completeness PASS
- Prompt variant (if applicable): Standard /sp.plan workflow with user-provided detailed plan outline
- Next experiment (smallest change to try): Proceed to /sp.tasks for task breakdown, then use specialized agents (secure-auth-agent, backend-engineer, nextjs-ui-builder) for implementation

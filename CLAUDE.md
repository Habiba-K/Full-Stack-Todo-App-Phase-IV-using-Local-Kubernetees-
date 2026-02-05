# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Project Context: Phase II Todo Full-Stack Web Application

**Project Overview:**
Transform a console-based todo application into a modern multi-user web application with persistent storage using the Agentic Dev Stack workflow.

**Tech Stack:**
- **Frontend:** Next.js (React-based framework)
- **Backend:** FastAPI (Python web framework)
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth
- **Development Approach:** Spec-Driven Development (no manual coding)

**Core Requirements:**
- Implement all Basic Level features as a web application
- Create RESTful API endpoints
- Build responsive frontend interface
- Store data in Neon Serverless PostgreSQL database
- Implement user signup/signin using Better Auth
- Multi-user support with data isolation

**Workflow Mandate:**
Follow the Agentic Dev Stack workflow strictly:
1. Write spec (using `/sp.specify`)
2. Generate plan (using `/sp.plan`)
3. Break into tasks (using `/sp.tasks`)
4. Implement via Claude Code (using `/sp.implement`)
5. NO manual coding allowed - all development through agents

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Specialized Agent Usage

For this project, you MUST use specialized agents for their respective domains. These agents have deep expertise and should be invoked proactively.

### 1. Authentication Agent (`secure-auth-agent`)
**Use for:**
- User signup/signin/logout flows
- Better Auth integration and configuration
- Password hashing and validation
- JWT/session token management
- Access control and authorization logic
- Security vulnerability prevention (XSS, CSRF, SQL injection)
- Authentication middleware implementation

**When to invoke:**
- ANY authentication-related feature implementation
- Security reviews of auth endpoints
- User session management
- Password reset/change functionality
- Role-based access control (RBAC)

**Example invocation:**
```
Use Task tool with subagent_type="secure-auth-agent"
Prompt: "Implement user signup and signin using Better Auth with FastAPI backend"
```

### 2. Frontend Agent (`nextjs-ui-builder`)
**Use for:**
- Building Next.js pages and components
- Responsive UI design and layouts
- React component development
- Form creation and validation (client-side)
- State management (React hooks, context)
- Client-side routing
- UI/UX implementation
- Styling (CSS, Tailwind, etc.)

**When to invoke:**
- Creating new pages or UI components
- Implementing responsive designs
- Building forms and interactive elements
- Optimizing frontend performance
- Adding client-side interactivity

**Example invocation:**
```
Use Task tool with subagent_type="nextjs-ui-builder"
Prompt: "Create a responsive todo list page with add, edit, delete functionality"
```

### 3. Database Agent (`neon-db-expert`)
**Use for:**
- Neon Serverless PostgreSQL schema design
- Database migrations
- Table creation and relationships
- Indexing strategies
- Query optimization
- Connection pooling configuration
- Data modeling and normalization
- Database constraints and triggers

**When to invoke:**
- Designing database schema
- Creating or modifying tables
- Performance issues with queries
- Migration creation and execution
- Database connection problems
- Data integrity concerns

**Example invocation:**
```
Use Task tool with subagent_type="neon-db-expert"
Prompt: "Design database schema for multi-user todo app with users, todos, and categories tables"
```

### 4. Backend Agent (`backend-engineer`)
**Use for:**
- FastAPI route implementation
- RESTful API design
- Request/response handling
- API validation and error handling
- Business logic implementation
- Database query integration
- API documentation (OpenAPI/Swagger)
- Server-side performance optimization

**When to invoke:**
- Creating API endpoints
- Implementing business logic
- API performance issues
- Request validation
- Error handling strategies
- API documentation needs

**Example invocation:**
```
Use Task tool with subagent_type="backend-engineer"
Prompt: "Create FastAPI endpoints for CRUD operations on todos with user authentication"
```

### Agent Coordination Strategy

**Multi-agent workflows:**
When a feature spans multiple domains, coordinate agents sequentially:

1. **Database First:** Use `neon-db-expert` to design schema
2. **Backend Second:** Use `backend-engineer` to create API endpoints
3. **Frontend Third:** Use `nextjs-ui-builder` to build UI
4. **Auth Integration:** Use `secure-auth-agent` to secure endpoints

**Example full-stack feature flow:**
```
Feature: User Todo Management

Step 1: Database Schema
- Agent: neon-db-expert
- Task: Design todos table with user_id foreign key

Step 2: API Endpoints
- Agent: backend-engineer
- Task: Create CRUD endpoints for todos

Step 3: Authentication
- Agent: secure-auth-agent
- Task: Add JWT middleware to protect todo endpoints

Step 4: Frontend UI
- Agent: nextjs-ui-builder
- Task: Build todo list page with forms
```

## Technology Stack Guidelines

### Next.js Frontend Best Practices
- Use App Router (not Pages Router) for new features
- Implement Server Components by default; use Client Components only when needed (interactivity, hooks)
- Use TypeScript for type safety
- Implement responsive design with Tailwind CSS or CSS modules
- Follow React best practices: component composition, proper state management
- Use Next.js built-in features: Image optimization, Link component, metadata API
- Implement proper error boundaries and loading states
- Use environment variables for API endpoints (NEXT_PUBLIC_ prefix for client-side)

### FastAPI Backend Best Practices
- Use Pydantic models for request/response validation
- Implement proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- Use dependency injection for database sessions and auth
- Implement comprehensive error handling with custom exception handlers
- Use async/await for database operations
- Document APIs with OpenAPI/Swagger (auto-generated by FastAPI)
- Implement CORS properly for Next.js frontend
- Use environment variables for sensitive configuration
- Structure: routers, models, schemas, services, dependencies

### Neon Serverless PostgreSQL Best Practices
- Use connection pooling (pgbouncer) for serverless environments
- Implement proper indexes for frequently queried columns
- Use foreign keys and constraints for data integrity
- Design schema with normalization principles
- Use migrations for schema changes (Alembic recommended)
- Implement soft deletes where appropriate (deleted_at column)
- Add created_at and updated_at timestamps to all tables
- Use UUIDs for primary keys in multi-tenant scenarios
- Optimize queries: avoid N+1 problems, use JOINs efficiently

### Better Auth Integration Best Practices
- Store hashed passwords only (never plain text)
- Implement JWT tokens with appropriate expiration
- Use refresh tokens for long-lived sessions
- Implement proper CORS and CSRF protection
- Validate tokens on every protected endpoint
- Use secure HTTP-only cookies for token storage
- Implement rate limiting on auth endpoints
- Add email verification for new accounts
- Implement password strength requirements
- Log authentication events for security auditing

### Multi-User Data Isolation
- Every data table must have a user_id foreign key
- Filter all queries by authenticated user_id
- Implement row-level security in database or application layer
- Never expose other users' data in API responses
- Validate user ownership before update/delete operations
- Use database transactions for multi-table operations
- Implement proper authorization checks (not just authentication)

## Phase II: Todo Application Requirements

### Core Features (Basic Level)
The application must implement these 5 basic features as a full-stack web application:

1. **Add Todo**
   - User can create a new todo item
   - Required fields: title, description (optional), due_date (optional)
   - Auto-assign to authenticated user
   - Return created todo with ID and timestamps

2. **View Todos**
   - List all todos for authenticated user only
   - Display: title, description, status, due_date, created_at
   - Support filtering (by status, due_date)
   - Support sorting (by created_at, due_date, priority)
   - Implement pagination for large lists

3. **Update Todo**
   - User can edit their own todos
   - Editable fields: title, description, status, due_date, priority
   - Validate user ownership before update
   - Return updated todo with new updated_at timestamp

4. **Delete Todo**
   - User can delete their own todos
   - Validate user ownership before deletion
   - Implement soft delete (recommended) or hard delete
   - Return success confirmation

5. **Mark Todo Complete/Incomplete**
   - Toggle todo status between "pending" and "completed"
   - Update completed_at timestamp when marked complete
   - Clear completed_at when marked incomplete
   - Validate user ownership

### Authentication Requirements
- **Signup:** Email, password, name (optional)
- **Signin:** Email and password authentication
- **Session Management:** JWT tokens with refresh capability
- **Protected Routes:** All todo endpoints require authentication
- **Logout:** Invalidate tokens properly

### Database Schema Requirements
Minimum required tables:

**users table:**
- id (UUID, primary key)
- email (unique, not null)
- password_hash (not null)
- name (optional)
- created_at (timestamp)
- updated_at (timestamp)

**todos table:**
- id (UUID, primary key)
- user_id (UUID, foreign key to users.id)
- title (string, not null)
- description (text, optional)
- status (enum: pending, completed)
- priority (enum: low, medium, high, optional)
- due_date (date, optional)
- completed_at (timestamp, optional)
- created_at (timestamp)
- updated_at (timestamp)
- deleted_at (timestamp, optional for soft delete)

### API Endpoints Requirements

**Authentication Endpoints:**
- POST /api/auth/signup - Create new user account
- POST /api/auth/signin - Authenticate and return JWT
- POST /api/auth/logout - Invalidate session
- GET /api/auth/me - Get current user info

**Todo Endpoints (all require authentication):**
- POST /api/todos - Create new todo
- GET /api/todos - List user's todos (with filters, pagination)
- GET /api/todos/{id} - Get single todo by ID
- PUT /api/todos/{id} - Update todo
- DELETE /api/todos/{id} - Delete todo
- PATCH /api/todos/{id}/complete - Mark todo as complete
- PATCH /api/todos/{id}/incomplete - Mark todo as incomplete

### Frontend Pages Requirements

**Public Pages:**
- /signup - User registration form
- /signin - User login form

**Protected Pages (require authentication):**
- /dashboard - Main todo list view with filters
- /todos/new - Create new todo form
- /todos/[id]/edit - Edit existing todo form
- /profile - User profile and settings

### UI/UX Requirements
- Responsive design (mobile, tablet, desktop)
- Loading states for async operations
- Error messages for validation failures
- Success notifications for actions
- Confirmation dialogs for destructive actions (delete)
- Form validation with clear error messages
- Accessible UI (ARIA labels, keyboard navigation)

### Security Requirements
- Password hashing (bcrypt or argon2)
- JWT token validation on all protected endpoints
- CORS configuration for frontend-backend communication
- Input validation and sanitization
- SQL injection prevention (use parameterized queries)
- XSS prevention (escape user input)
- CSRF protection
- Rate limiting on authentication endpoints
- Secure environment variable management

### Testing Requirements
- Unit tests for critical business logic
- Integration tests for API endpoints
- Authentication flow testing
- Database query testing
- Error handling testing

### Deployment Considerations
- Environment variables for configuration
- Database connection pooling
- Error logging and monitoring
- API documentation (Swagger/OpenAPI)
- README with setup instructions

### Success Criteria
- All 5 basic features fully functional
- Multi-user support with complete data isolation
- Secure authentication with Better Auth
- Responsive UI works on all device sizes
- All API endpoints properly documented
- No security vulnerabilities (XSS, SQL injection, etc.)
- Code follows best practices for each technology
- Proper error handling throughout the application

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

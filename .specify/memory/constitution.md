# AI Todo Chatbot Constitution (Phase-III)

<!--
Sync Impact Report:
- Version: 1.0.0 → 2.0.0
- Type: MAJOR - Backward incompatible architectural redefinition
- Modified Principles:
  - I. Security-First Design → Updated for agent-based auth and MCP tool security
  - II. Correctness and Reliability → Redefined for stateless, conversation-driven architecture
  - III. Clean Architecture → Completely redefined for Agent/MCP/API/UI separation
  - IV. Maintainability → Updated for agent and MCP tool patterns
  - V. Modern Full-Stack Standards → Replaced with AI-First Conversational Standards
  - VI. Test-Driven Development → Retained with agent-specific testing additions
- Added Sections:
  - Stateless Architecture Mandate (new core principle)
  - MCP Tool Requirements (new technology constraint)
  - OpenAI Agents SDK Requirements (new technology constraint)
  - Agent Behavior Standards (new quality standard)
  - Conversation Persistence Requirements (new functional requirement)
- Removed Sections:
  - Traditional REST API endpoint requirements (replaced with agent-driven operations)
  - Next.js frontend requirements (replaced with OpenAI ChatKit)
  - Direct database access patterns (replaced with MCP-only access)
- Templates Status:
  ⚠ plan-template.md - Requires update: Constitution Check gates must reflect stateless + MCP principles
  ⚠ spec-template.md - Requires update: User stories must be conversational scenarios, not UI interactions
  ⚠ tasks-template.md - Requires update: Task categories must include MCP tool creation, agent configuration
- Follow-up TODOs:
  - Update plan-template.md Constitution Check section with Phase-III gates
  - Update spec-template.md to guide conversational user story writing
  - Update tasks-template.md to include MCP and agent task categories
-->

## Core Principles

### I. Security-First Design

All authentication and authorization logic MUST enforce user isolation at every layer. JWT tokens MUST be verified on every API request using the shared BETTER_AUTH_SECRET. The authenticated user identity MUST be passed to all MCP tool invocations. MCP tools MUST filter all database queries by authenticated user ID. AI agents MUST NOT access the database directly. No user may access another user's data under any condition. Agent prompts MUST NOT leak user data across conversations.

**Rationale**: Multi-user AI systems require strict data isolation to prevent unauthorized access, prompt injection attacks, and cross-user data leakage. Security violations are non-negotiable and must be prevented by design at the MCP tool layer.

### II. Stateless Architecture Mandate

The FastAPI backend MUST be completely stateless with respect to conversation context and user sessions. All conversation history MUST be stored in the database and rebuilt from the database on every request. The server MUST NOT hold any in-memory conversation state, agent state, or user session state beyond JWT validation. Every API request MUST be independently processable using only the JWT token and database state.

**Rationale**: Stateless architecture enables horizontal scaling, simplifies deployment, prevents memory leaks, and ensures conversation persistence across server restarts. This is critical for production AI systems.

### III. Clean Separation of Concerns

The system MUST maintain strict separation between four layers: Agent (AI decision-making), MCP Tools (data operations), API (request handling), and UI (user interface). OpenAI Agents SDK handles AI reasoning and tool selection. MCP tools are the ONLY mechanism for data mutations and queries. FastAPI handles HTTP requests, JWT validation, and agent orchestration. OpenAI ChatKit provides the conversational UI. No layer may bypass or duplicate responsibilities of another layer.

**Rationale**: Clear separation enables independent testing, prevents tight coupling, and ensures the AI agent cannot directly manipulate data without going through validated MCP tools. This architecture pattern is essential for auditable and secure AI systems.

### IV. MCP Tool-Only Data Access

All task operations (create, read, update, delete, list, filter) MUST be implemented as MCP tools. The AI agent MUST NOT have direct database access. The FastAPI backend MUST NOT implement task logic outside of MCP tool definitions. All business rules and data validation MUST be enforced within MCP tools. The agent selects which tool to use based on user intent; the tool executes the validated operation.

**Rationale**: Centralizing data operations in MCP tools creates a single, auditable, testable layer for all data mutations. This prevents the agent from bypassing validation, enables tool-level security checks, and simplifies debugging.

### V. Conversation-Driven Design

Users MUST interact with the system exclusively through natural language conversation. The AI agent MUST interpret user intent and select appropriate MCP tools. All actions MUST be confirmed in natural language responses. The system MUST maintain conversation context across multiple turns. Error messages MUST be conversational and actionable, not technical error codes.

**Rationale**: Natural language interfaces reduce cognitive load, eliminate the need for UI training, and enable more intuitive task management. Conversational design is the core value proposition of AI-driven applications.

### VI. Database as Single Source of Truth

The Neon PostgreSQL database MUST be the authoritative source for all user data, todos, and conversation history. Conversation context MUST be rebuilt from the database on every request. No caching of conversation state is permitted in the backend. All MCP tool operations MUST immediately persist to the database. The system MUST be able to resume conversations after server restarts without data loss.

**Rationale**: Database-first design ensures data durability, enables stateless backend architecture, and prevents data loss during deployments or crashes. This is non-negotiable for production systems.

### VII. Maintainability and Testability

MCP tools MUST be independently testable without requiring the full agent. Each MCP tool MUST have clear input schemas and output schemas. Agent behavior MUST be testable through conversation scenarios. Backend MUST use clear module separation: routers, services, MCP tool definitions, database models. Configuration MUST use environment variables (no hardcoded secrets). Code MUST be readable with clear naming conventions.

**Rationale**: Maintainable code reduces technical debt and enables team scalability. Clear structure allows new developers to contribute quickly. Independent testability of MCP tools is critical for reliable AI systems.

## Technology Stack Requirements

**Mandatory Technologies**:
- Frontend: OpenAI ChatKit (conversational UI)
- Backend: Python FastAPI with async/await
- AI: OpenAI Agents SDK (agent orchestration and tool selection)
- MCP: Official MCP SDK (Model Context Protocol for tool definitions)
- Database: Neon Serverless PostgreSQL with connection pooling
- Authentication: Better Auth (JWT token generation and validation)

**Technology Constraints**:
- Use Pydantic models for all MCP tool input/output schemas
- Use SQLModel for database operations within MCP tools
- Backend must be async (async/await) for all I/O operations
- Use environment variables for all configuration (OPENAI_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET)
- Implement CORS properly for ChatKit-backend communication
- Use connection pooling (pgbouncer) for Neon database

**Prohibited Practices**:
- No direct database access from AI agent (MUST use MCP tools)
- No server-side conversation state storage (MUST rebuild from DB)
- No hardcoded task logic outside MCP tools
- No plain text password storage (hashing required)
- No hardcoded secrets or API keys in code
- No SQL string concatenation (use parameterized queries only)
- No bypassing authentication on protected endpoints
- No exposing other users' data in API responses or agent context

## Functional Requirements

**Core Features (Natural Language Interface)**:
The application MUST implement these 5 features through conversational AI:

1. **Add Todo**: User says "Add a task to buy groceries" → Agent uses create_todo MCP tool → Confirms "I've added 'buy groceries' to your todo list"
2. **View Todos**: User says "Show my tasks" → Agent uses list_todos MCP tool → Returns formatted list in natural language
3. **Update Todo**: User says "Change the grocery task to buy milk" → Agent uses update_todo MCP tool → Confirms update
4. **Delete Todo**: User says "Remove the milk task" → Agent uses delete_todo MCP tool → Confirms deletion
5. **Mark Complete**: User says "Mark the milk task as done" → Agent uses complete_todo MCP tool → Confirms completion

**MCP Tool Requirements**:
The system MUST implement these MCP tools (minimum):
- `create_todo`: Create new todo with title, description (optional), due_date (optional), user_id
- `list_todos`: List todos for user with optional filters (status, due_date) and sorting
- `get_todo`: Retrieve single todo by ID with user ownership validation
- `update_todo`: Update todo fields with user ownership validation
- `delete_todo`: Delete todo with user ownership validation
- `complete_todo`: Mark todo as complete with timestamp
- `incomplete_todo`: Mark todo as incomplete

**Authentication Requirements**:
- User signup with email, password, name (optional)
- User signin with email and password
- JWT token generation on successful signin
- JWT token validation on every API request
- User ID extraction from JWT and passed to all MCP tools
- Logout with proper token invalidation (client-side token removal)

**API Endpoint Requirements**:
- POST /api/auth/signup - Create new user account
- POST /api/auth/signin - Authenticate and return JWT
- POST /api/auth/logout - Invalidate session (client-side)
- GET /api/auth/me - Get current user info
- POST /api/chat - Main conversational endpoint (receives user message, returns agent response)
- GET /api/chat/history - Retrieve conversation history for user

**Database Schema Requirements**:
- **users table**: id (UUID), email (unique), password_hash, name, created_at, updated_at
- **todos table**: id (UUID), user_id (FK), title, description, status (enum: pending, completed), priority (enum: low, medium, high), due_date, completed_at, created_at, updated_at, deleted_at (optional)
- **conversations table**: id (UUID), user_id (FK), created_at, updated_at
- **messages table**: id (UUID), conversation_id (FK), role (enum: user, assistant), content (text), created_at

**Conversation Persistence Requirements**:
- All user messages MUST be stored in messages table with role='user'
- All agent responses MUST be stored in messages table with role='assistant'
- Conversation history MUST be loaded from database on every /api/chat request
- Conversation context MUST include recent messages (e.g., last 10 turns) for agent context
- Old conversations MUST be retrievable via /api/chat/history

**UI/UX Requirements**:
- Conversational interface with message bubbles (user vs assistant)
- Loading indicator while agent processes request
- Error messages displayed conversationally ("I couldn't complete that because...")
- Message history scrollable and persistent
- Input field for natural language commands
- Responsive design (mobile, tablet, desktop)

## Quality and Security Standards

**Security Requirements (NON-NEGOTIABLE)**:
- Password hashing with bcrypt or argon2
- JWT token validation on all protected endpoints
- User ID extraction from JWT and passed to all MCP tools
- MCP tools MUST validate user ownership before update/delete operations
- Input validation and sanitization on all inputs (both API and MCP tool level)
- SQL injection prevention (parameterized queries only)
- Prompt injection prevention (sanitize user input before passing to agent)
- Rate limiting on authentication endpoints
- Secure environment variable management
- Agent prompts MUST NOT include other users' data

**Agent Behavior Standards**:
- Agent MUST select appropriate MCP tool based on user intent
- Agent MUST confirm actions in natural language
- Agent MUST handle ambiguous requests by asking clarifying questions
- Agent MUST provide helpful error messages when operations fail
- Agent MUST NOT hallucinate todo items (only return data from MCP tools)
- Agent MUST NOT attempt to access database directly
- Agent responses MUST be concise and actionable

**Error Handling Standards**:
- 401 Unauthorized: Missing or invalid JWT token
- 403 Forbidden: User mismatch or ownership violation
- 404 Not Found: Nonexistent resource under user scope
- 422 Validation Error: Invalid request payload or MCP tool input
- 500 Internal Server Error: Unexpected server errors (with logging)
- Agent errors: Conversational error messages ("I couldn't find that task. Could you describe it differently?")

**Performance Standards**:
- Database connection pooling for serverless environment
- Proper indexes on frequently queried columns (user_id, status, due_date, conversation_id)
- Conversation history limited to recent messages (e.g., last 10 turns) to reduce token usage
- Agent response time target: <3 seconds for simple operations
- Optimize OpenAI API calls (use appropriate model, limit context size)

**Data Integrity Standards**:
- Foreign keys and constraints for referential integrity
- Timestamps (created_at, updated_at) on all tables
- Soft deletes where appropriate (deleted_at column)
- Database transactions for multi-table operations
- Validation at both API and MCP tool layers
- Conversation messages MUST be immutable (no updates, only inserts)

## Development Workflow

**Spec-Driven Development Mandate**:
All development MUST follow the Agentic Dev Stack workflow:
1. Write specification using `/sp.specify` (focus on conversational scenarios)
2. Generate implementation plan using `/sp.plan` (architecture for stateless + MCP)
3. Break into tasks using `/sp.tasks` (include MCP tool creation tasks)
4. Implement via Claude Code using `/sp.implement`
5. NO manual coding allowed - all development through agents

**Agent Usage Requirements**:
- Use `secure-auth-agent` for authentication and JWT validation work
- Use `backend-engineer` for FastAPI endpoints and agent orchestration
- Use `neon-db-expert` for database schema and MCP tool database operations
- Use specialized agents for MCP tool creation and testing
- Coordinate agents sequentially: Database → MCP Tools → Backend → Agent Integration → UI

**MCP Tool Development Standards**:
- Each MCP tool MUST have a clear, single responsibility
- MCP tool input schemas MUST use Pydantic models with validation
- MCP tool output schemas MUST be consistent and documented
- MCP tools MUST include user_id parameter for all data operations
- MCP tools MUST validate user ownership before mutations
- MCP tools MUST be independently testable (unit tests without agent)
- MCP tools MUST log all operations for debugging

**Agent Integration Standards**:
- Agent system prompt MUST clearly describe available MCP tools
- Agent MUST be tested with conversation scenarios (not just unit tests)
- Agent behavior MUST be validated for common user intents
- Agent MUST handle edge cases gracefully (ambiguous requests, missing data)
- Agent responses MUST be reviewed for hallucination prevention

**Code Review Standards**:
- All changes must reference specific user stories or requirements
- Security-sensitive code (auth, MCP tools, data access) requires extra scrutiny
- Database migrations must be reversible
- MCP tool changes must maintain backward compatibility or be versioned
- Agent prompt changes must be tested with conversation scenarios
- Statelessness must be verified (no in-memory state)

**Documentation Requirements**:
- MCP tools documented with input/output schemas and examples
- Agent system prompt documented with tool descriptions
- API endpoints documented with OpenAPI/Swagger (auto-generated by FastAPI)
- README with setup instructions and environment variables
- Database schema documented in migrations
- Conversation flow examples documented for testing

## Governance

**Constitution Authority**:
This constitution supersedes all other development practices and guidelines. When conflicts arise between this document and other sources, this constitution takes precedence.

**Amendment Process**:
1. Proposed amendments must be documented with rationale
2. Impact analysis required for all dependent templates and code
3. Version must be incremented according to semantic versioning:
   - MAJOR: Backward incompatible principle removals or redefinitions
   - MINOR: New principles or materially expanded guidance
   - PATCH: Clarifications, wording fixes, non-semantic refinements
4. All amendments must update LAST_AMENDED_DATE

**Compliance Verification**:
- All pull requests must verify compliance with security principles
- Code reviews must check for principle violations
- Statelessness must be verified (no server-side conversation state)
- MCP tool-only data access must be enforced (no direct DB access from agent)
- Complexity that violates principles must be explicitly justified in plan.md
- Constitution Check section in plan-template.md must be completed before implementation

**Enforcement**:
- Principle violations in security, statelessness, or MCP tool architecture are blocking issues
- Agent behavior violations (hallucination, direct DB access) are blocking issues
- Maintainability and standards violations should be addressed but may not block if justified
- All justifications for principle violations must be documented in Complexity Tracking section

**Version**: 2.0.0 | **Ratified**: 2026-01-22 | **Last Amended**: 2026-01-27

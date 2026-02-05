# Tasks: Authentication + JWT Security

**Input**: Design documents from `/specs/001-auth-jwt-security/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are recommended for security-critical auth flows but not explicitly required in specification. Test tasks are included as optional.

**Organization**: Tasks are grouped by user story to enable incremental delivery. Note that some stories have dependencies on earlier stories due to the nature of authentication (e.g., signin requires signup, protected access requires authentication).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install backend dependencies: fastapi, uvicorn, pyjwt, bcrypt, sqlmodel, asyncpg, python-dotenv in backend/
- [ ] T002 [P] Install frontend dependencies: better-auth in frontend/
- [x] T003 [P] Create backend/.env.example with BETTER_AUTH_SECRET, DATABASE_URL, CORS_ORIGINS placeholders
- [ ] T004 [P] Create frontend/.env.local.example with BETTER_AUTH_SECRET, NEXTAUTH_URL, NEXT_PUBLIC_API_URL placeholders
- [x] T005 Generate cryptographically secure BETTER_AUTH_SECRET (32+ characters) and add to both .env files
- [x] T006 [P] Update backend/.gitignore to exclude .env file
- [ ] T007 [P] Update frontend/.gitignore to exclude .env.local file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create users table in Neon PostgreSQL with schema from data-model.md (id, email, password_hash, name, created_at, updated_at)
- [x] T009 [P] Create indexes on users table: idx_users_email (unique), idx_users_created_at
- [x] T010 [P] Create backend/src/auth/ directory structure (__init__.py, dependencies.py, schemas.py, utils.py)
- [x] T011 [P] Create backend/src/models/user.py with User SQLModel matching database schema
- [x] T012 [P] Configure CORS middleware in backend/src/main.py to allow Authorization header from frontend origin
- [x] T013 [P] Create standardized error response format in backend/src/auth/schemas.py (ErrorResponse with detail, error_code, status_code)
- [x] T014 [P] Implement custom HTTPException handlers in backend/src/main.py for 401/403/422/500 errors

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email and password

**Independent Test**: Submit registration form with valid credentials and verify user account created in database

### Implementation for User Story 1

- [x] T015 [P] [US1] Create SignupRequest schema in backend/src/auth/schemas.py (email, password, name optional)
- [x] T016 [P] [US1] Create SignupResponse schema in backend/src/auth/schemas.py (id, email, name, created_at)
- [x] T017 [US1] Implement password hashing utility in backend/src/auth/utils.py using bcrypt with cost factor 12
- [x] T018 [US1] Implement POST /api/auth/signup endpoint in backend/src/routers/auth.py per auth-signup.yaml contract
- [x] T019 [US1] Add email uniqueness validation in signup endpoint (return 409 if email exists)
- [x] T020 [US1] Add password strength validation in signup endpoint (minimum 8 characters)
- [ ] T021 [P] [US1] Create frontend/src/components/auth/SignupForm.tsx with email, password, name fields
- [ ] T022 [US1] Create frontend/src/app/signup/page.tsx using SignupForm component
- [ ] T023 [US1] Implement form submission in SignupForm calling POST /api/auth/signup
- [ ] T024 [US1] Add client-side validation for email format and password length in SignupForm
- [ ] T025 [US1] Add error handling in SignupForm for 409 (email exists) and 422 (validation errors)
- [ ] T026 [US1] Add success message and redirect to signin page after successful signup

**Checkpoint**: Users can now create accounts. Test by registering a new user and verifying in database.

---

## Phase 4: User Story 2 - User Authentication (Priority: P1)

**Goal**: Enable registered users to sign in and receive JWT tokens for API access

**Independent Test**: Submit valid credentials and verify JWT token is issued and stored

### Implementation for User Story 2

- [x] T027 [P] [US2] Create SigninRequest schema in backend/src/auth/schemas.py (email, password)
- [x] T028 [P] [US2] Create SigninResponse schema in backend/src/auth/schemas.py (user, token, expires_at)
- [x] T029 [P] [US2] Create UserResponse schema in backend/src/auth/schemas.py (id, email, name, created_at, updated_at)
- [x] T030 [US2] Implement password verification utility in backend/src/auth/utils.py using bcrypt.checkpw
- [ ] T031 [US2] Configure Better Auth in frontend/src/lib/auth.ts with JWT enabled, 7-day expiration, BETTER_AUTH_SECRET
- [x] T032 [US2] Implement POST /api/auth/signin endpoint in backend/src/routers/auth.py per auth-signin.yaml contract
- [x] T033 [US2] Add credential validation in signin endpoint (verify email exists and password matches)
- [x] T034 [US2] Generate JWT token in signin endpoint with payload: sub (user_id), email, iat, exp using PyJWT
- [x] T035 [US2] Return 401 for invalid credentials in signin endpoint (don't reveal if email exists)
- [x] T036 [US2] Implement POST /api/auth/logout endpoint in backend/src/routers/auth.py per auth-logout.yaml contract
- [x] T037 [US2] Implement GET /api/auth/me endpoint in backend/src/routers/auth.py per auth-me.yaml contract
- [x] T038 [P] [US2] Create JWT verification dependency in backend/src/auth/dependencies.py using HTTPBearer and PyJWT
- [x] T039 [US2] Add JWT signature verification in dependency using BETTER_AUTH_SECRET and HS256 algorithm
- [x] T040 [US2] Handle JWT errors in dependency: ExpiredSignatureError → 401, InvalidTokenError → 401
- [x] T041 [US2] Extract user_id from JWT payload in dependency and return as dict
- [x] T042 [US2] Apply JWT verification dependency to GET /api/auth/me endpoint
- [ ] T043 [P] [US2] Create frontend/src/lib/api-client.ts with fetch wrapper that injects Authorization Bearer token
- [ ] T044 [US2] Implement token extraction from Better Auth session in api-client.ts
- [ ] T045 [P] [US2] Create frontend/src/components/auth/SigninForm.tsx with email and password fields
- [ ] T046 [US2] Create frontend/src/app/signin/page.tsx using SigninForm component
- [ ] T047 [US2] Implement form submission in SigninForm calling POST /api/auth/signin via api-client
- [ ] T048 [US2] Store JWT token in Better Auth session after successful signin
- [ ] T049 [US2] Add error handling in SigninForm for 401 (invalid credentials)
- [ ] T050 [US2] Redirect to dashboard after successful signin

**Checkpoint**: Users can now sign in and receive JWT tokens. Test by signing in and verifying token in response.

---

## Phase 5: User Story 3 - Protected Resource Access (Priority: P1)

**Goal**: Ensure only authenticated users with valid JWT tokens can access task endpoints

**Independent Test**: Make API requests with valid/invalid tokens and verify 401 responses for missing/invalid tokens

### Implementation for User Story 3

- [x] T051 [P] [US3] Add JWT verification dependency to GET /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py
- [x] T052 [P] [US3] Add JWT verification dependency to POST /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py
- [x] T053 [P] [US3] Add JWT verification dependency to GET /api/{user_id}/tasks/{id} endpoint in backend/src/routers/tasks.py
- [x] T054 [P] [US3] Add JWT verification dependency to PUT /api/{user_id}/tasks/{id} endpoint in backend/src/routers/tasks.py
- [x] T055 [P] [US3] Add JWT verification dependency to DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/routers/tasks.py
- [x] T056 [P] [US3] Add JWT verification dependency to PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/routers/tasks.py
- [x] T057 [US3] Update all task endpoint database queries to filter by authenticated user_id from JWT payload
- [x] T058 [US3] Test all task endpoints return 401 when Authorization header is missing
- [x] T059 [US3] Test all task endpoints return 401 when JWT token is invalid or expired
- [ ] T060 [P] [US3] Update frontend task API calls to use api-client.ts (automatic token injection)
- [ ] T061 [US3] Add 401 error handling in frontend to redirect to signin page when token is missing/invalid

**Checkpoint**: All task endpoints now require valid JWT tokens. Test by accessing endpoints without token (expect 401).

---

## Phase 6: User Story 4 - Ownership Enforcement (Priority: P1)

**Goal**: Validate that authenticated users can only access their own data, preventing cross-user access

**Independent Test**: Attempt to access resources with mismatched user_id in path parameters and verify 403 responses

### Implementation for User Story 4

- [x] T062 [US4] Create ownership validation utility in backend/src/auth/utils.py (compare path user_id to JWT user_id)
- [x] T063 [P] [US4] Add ownership validation to GET /api/{user_id}/tasks endpoint (return 403 if user_id mismatch)
- [x] T064 [P] [US4] Add ownership validation to POST /api/{user_id}/tasks endpoint (return 403 if user_id mismatch)
- [x] T065 [P] [US4] Add ownership validation to GET /api/{user_id}/tasks/{id} endpoint (return 403 if user_id mismatch)
- [x] T066 [P] [US4] Add ownership validation to PUT /api/{user_id}/tasks/{id} endpoint (return 403 if user_id mismatch)
- [x] T067 [P] [US4] Add ownership validation to DELETE /api/{user_id}/tasks/{id} endpoint (return 403 if user_id mismatch)
- [x] T068 [P] [US4] Add ownership validation to PATCH /api/{user_id}/tasks/{id}/complete endpoint (return 403 if user_id mismatch)
- [x] T069 [US4] Ensure all task database queries remain scoped by authenticated user_id (double-check filtering)
- [x] T070 [US4] Test cross-user access attempts return 403 for all task endpoints
- [x] T071 [US4] Test same-user access succeeds for all task endpoints

**Checkpoint**: Ownership enforcement complete. Test by creating two users and attempting cross-user access (expect 403).

---

## Phase 7: User Story 5 - Token Expiration Handling (Priority: P2)

**Goal**: Gracefully handle expired JWT tokens and prompt re-authentication

**Independent Test**: Use expired token and verify 401 response with clear expiration message, then re-authenticate successfully

### Implementation for User Story 5

- [ ] T072 [P] [US5] Update JWT verification dependency to return specific error message for ExpiredSignatureError
- [ ] T073 [P] [US5] Create frontend auth middleware in frontend/src/middleware.ts to protect dashboard routes
- [ ] T074 [US5] Add token expiration check in frontend middleware (redirect to signin if expired)
- [ ] T075 [US5] Update frontend 401 error handler to distinguish between missing token and expired token
- [ ] T076 [US5] Display user-friendly expiration message in frontend when token expires
- [ ] T077 [US5] Clear Better Auth session on token expiration in frontend
- [ ] T078 [US5] Test token expiration flow: expired token → 401 → redirect to signin → re-authenticate → new token

**Checkpoint**: Token expiration handled gracefully. Test by manually expiring a token or waiting for expiration.

---

## Phase 8: Testing & Validation (Optional - Recommended for Security)

**Purpose**: Comprehensive testing of authentication flows and security enforcement

**Note**: These tests are recommended but not required by specification

- [ ] T079 [P] Create backend/tests/test_auth_endpoints.py for auth endpoint integration tests
- [ ] T080 [P] Test signup endpoint: valid credentials → 201, duplicate email → 409, weak password → 422
- [ ] T081 [P] Test signin endpoint: valid credentials → 200 with token, invalid credentials → 401
- [ ] T082 [P] Test logout endpoint: valid token → 200, no token → 401
- [ ] T083 [P] Test me endpoint: valid token → 200 with user info, invalid token → 401
- [ ] T084 [P] Create backend/tests/test_ownership.py for ownership enforcement tests
- [ ] T085 [P] Test cross-user access prevention: user A token + user B path → 403 for all endpoints
- [ ] T086 [P] Test same-user access: user A token + user A path → 200 for all endpoints
- [ ] T087 [P] Test token tampering: modified signature → 401, modified payload → 401
- [ ] T088 [P] Test edge cases: malformed token → 401, missing Bearer prefix → 401, empty token → 401

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, cleanup, and final validation

- [ ] T089 [P] Update README.md with authentication setup instructions from quickstart.md
- [ ] T090 [P] Document environment variables in README: BETTER_AUTH_SECRET, DATABASE_URL, CORS_ORIGINS, NEXTAUTH_URL
- [ ] T091 [P] Add authentication flow diagram to README (signup → signin → JWT → protected access)
- [ ] T092 [P] Document error responses in README: 401 (auth failure), 403 (ownership violation)
- [ ] T093 [P] Create production deployment checklist in README (HTTPS, secret rotation, CORS config)
- [ ] T094 Validate all tasks completed by running through quickstart.md test scenarios
- [ ] T095 [P] Code review: verify no hardcoded secrets, all passwords hashed, all queries scoped by user_id
- [ ] T096 [P] Security audit: verify JWT verification on all protected endpoints, ownership validation on all user-scoped endpoints
- [ ] T097 Run full authentication flow end-to-end: signup → signin → access protected resource → logout

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) AND User Story 1 (needs users to authenticate)
- **User Story 3 (Phase 5)**: Depends on User Story 2 (needs JWT verification infrastructure)
- **User Story 4 (Phase 6)**: Depends on User Story 3 (needs protected endpoints to enforce ownership)
- **User Story 5 (Phase 7)**: Depends on User Story 2 (needs JWT infrastructure for expiration handling)
- **Testing (Phase 8)**: Depends on all user stories being complete
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Foundational (Phase 2)
    ↓
User Story 1: Registration (Phase 3) - Independent
    ↓
User Story 2: Authentication (Phase 4) - Depends on US1
    ↓
    ├─→ User Story 3: Protected Access (Phase 5) - Depends on US2
    │       ↓
    │   User Story 4: Ownership (Phase 6) - Depends on US3
    │
    └─→ User Story 5: Token Expiration (Phase 7) - Depends on US2
```

### Within Each User Story

- Backend schemas before endpoints
- Utilities before endpoints that use them
- Backend endpoints before frontend integration
- Frontend components before pages
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: Tasks T002-T007 can run in parallel

**Phase 2 (Foundational)**: Tasks T009-T014 can run in parallel after T008 completes

**Phase 3 (US1)**:
- T015, T016, T021 can run in parallel
- T022-T026 can run in parallel after T021 completes

**Phase 4 (US2)**:
- T027-T029, T038, T043, T045 can run in parallel
- T051-T056 (Phase 5) can run in parallel after US2 backend complete

**Phase 5 (US3)**: Tasks T051-T056 can run in parallel, T060 can run in parallel

**Phase 6 (US4)**: Tasks T063-T068 can run in parallel after T062 completes

**Phase 7 (US5)**: Tasks T072-T073 can run in parallel

**Phase 8 (Testing)**: All test tasks T079-T088 can run in parallel

**Phase 9 (Polish)**: Tasks T089-T093, T095-T096 can run in parallel

---

## Parallel Example: User Story 2 (Authentication)

```bash
# After Foundational phase completes, these can run in parallel:

# Terminal 1: Backend schemas
Task T027, T028, T029 - Create request/response schemas

# Terminal 2: Backend utilities
Task T030 - Password verification utility
Task T038 - JWT verification dependency

# Terminal 3: Frontend infrastructure
Task T031 - Better Auth configuration
Task T043 - API client with token injection
Task T045 - SigninForm component

# Then sequentially:
Task T032-T037 - Backend endpoints (use schemas and utilities)
Task T039-T042 - JWT verification (use dependency)
Task T046-T050 - Frontend pages (use components and api-client)
```

---

## MVP Scope Recommendation

**Minimum Viable Product**: Phases 1-6 (Setup through User Story 4)

This delivers:
- ✅ User registration and account creation
- ✅ User authentication with JWT tokens
- ✅ Protected API endpoints requiring authentication
- ✅ Ownership enforcement preventing cross-user access
- ✅ Core security features operational

**Phase 7 (Token Expiration)** is P2 and can be added after MVP validation.

**Phase 8 (Testing)** is recommended for production but optional for MVP demo.

**Phase 9 (Polish)** should be completed before production deployment.

---

## Task Summary

- **Total Tasks**: 97 tasks
- **Setup**: 7 tasks
- **Foundational**: 7 tasks
- **User Story 1 (Registration)**: 12 tasks
- **User Story 2 (Authentication)**: 24 tasks
- **User Story 3 (Protected Access)**: 11 tasks
- **User Story 4 (Ownership)**: 10 tasks
- **User Story 5 (Token Expiration)**: 7 tasks
- **Testing**: 10 tasks (optional)
- **Polish**: 9 tasks

**Parallel Opportunities**: 45 tasks marked [P] can run in parallel within their phase

**Independent Testing**:
- US1: Test signup creates user in database
- US2: Test signin returns JWT token
- US3: Test endpoints require valid token (401 without)
- US4: Test cross-user access blocked (403)
- US5: Test expired token handling (401 with clear message)

**Format Validation**: ✅ All tasks follow checklist format with ID, optional [P], optional [Story], and file paths

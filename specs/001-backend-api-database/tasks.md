---

description: "Task list for Backend REST API + Database implementation"
---

# Tasks: Backend REST API + Database

**Input**: Design documents from `/specs/001-backend-api-database/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT requested in the feature specification, so test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/` at repository root
- Paths shown below use backend structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (backend/src/, backend/src/models/, backend/src/schemas/, backend/src/routers/, backend/src/services/)
- [x] T002 Create requirements.txt with dependencies (fastapi==0.109.0, uvicorn[standard]==0.27.0, sqlmodel==0.0.14, psycopg2-binary==2.9.9, python-dotenv==1.0.0)
- [x] T003 [P] Create .env.example file with DATABASE_URL placeholder in backend/
- [x] T004 [P] Create README.md with setup instructions in backend/
- [x] T004a [P] Create .gitignore file with Python, environment, and IDE exclusions at repository root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create config.py with Settings class for environment variables in backend/src/
- [x] T006 Create database.py with SQLModel engine and session setup (async, Neon connection with pgbouncer) in backend/src/
- [x] T007 Create dependencies.py with get_db() async session dependency in backend/src/
- [x] T008 Create Task model (SQLModel) with all fields (id, user_id, title, description, completed, created_at, updated_at) in backend/src/models/task.py
- [x] T009 [P] Create TaskResponse schema (Pydantic) for API responses in backend/src/schemas/task.py
- [x] T010 Create main.py with FastAPI app initialization, CORS configuration, and startup event to create tables in backend/src/
- [x] T011 Add tasks router to main.py (import and include_router)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - List User Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable retrieval of all tasks for a specific user to verify data persistence and user ownership enforcement

**Independent Test**: Make GET request to /api/{user_id}/tasks with a user ID and verify only that user's tasks are returned in structured JSON format

### Implementation for User Story 1

- [x] T012 [US1] Implement get_user_tasks() service method in backend/src/services/task_service.py (query tasks filtered by user_id, return list)
- [x] T013 [US1] Implement GET /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py (call service, return TaskResponse list, status 200)
- [x] T014 [US1] Add error handling for database connection errors in list endpoint

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Create New Task (Priority: P2)

**Goal**: Enable creation of new tasks for a specific user to verify write operations and data persistence

**Independent Test**: Make POST request with task data and verify task is created, assigned to correct user, and persisted in database

### Implementation for User Story 2

- [x] T015 [P] [US2] Create TaskCreate schema (Pydantic) with title and optional description in backend/src/schemas/task.py
- [x] T016 [US2] Implement create_task() service method in backend/src/services/task_service.py (create Task with user_id, save to DB, return created task)
- [x] T017 [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py (validate TaskCreate, call service, return TaskResponse, status 201)
- [x] T018 [US2] Add validation error handling (422) for missing/invalid title in create endpoint

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - View Single Task Details (Priority: P3)

**Goal**: Enable retrieval of specific task details to verify individual record access and ownership enforcement

**Independent Test**: Make GET request with task ID and user ID, verify correct task details returned and ownership enforced (404 for other users)

### Implementation for User Story 3

- [x] T019 [US3] Implement get_task_by_id() service method in backend/src/services/task_service.py (query task by id AND user_id, return task or None)
- [x] T020 [US3] Implement GET /api/{user_id}/tasks/{task_id} endpoint in backend/src/routers/tasks.py (call service, return TaskResponse or 404)
- [x] T021 [US3] Add error handling for task not found (404) and ownership violations in get endpoint

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Existing Task (Priority: P4)

**Goal**: Enable modification of existing task details to verify update operations and data persistence

**Independent Test**: Make PUT request with updated data and verify changes are persisted and returned correctly

### Implementation for User Story 4

- [x] T022 [P] [US4] Create TaskUpdate schema (Pydantic) with optional title, description, completed in backend/src/schemas/task.py
- [x] T023 [US4] Implement update_task() service method in backend/src/services/task_service.py (find task by id AND user_id, update fields, save, return updated task or None)
- [x] T024 [US4] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/src/routers/tasks.py (validate TaskUpdate, call service, return TaskResponse or 404)
- [x] T025 [US4] Add validation error handling (422) for invalid update data and ownership enforcement (404) in update endpoint

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: Enable removal of tasks from the system to verify delete operations work correctly

**Independent Test**: Make DELETE request and verify task is removed from database and no longer appears in queries

### Implementation for User Story 5

- [x] T026 [US5] Implement delete_task() service method in backend/src/services/task_service.py (find task by id AND user_id, delete from DB, return success boolean)
- [x] T027 [US5] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/src/routers/tasks.py (call service, return success message or 404)
- [x] T028 [US5] Add error handling for task not found (404) and ownership enforcement in delete endpoint

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Toggle Task Completion Status (Priority: P6)

**Goal**: Enable marking tasks as complete/incomplete to verify partial update operations work correctly

**Independent Test**: Make PATCH request to toggle completion status and verify status change is persisted

### Implementation for User Story 6

- [x] T029 [US6] Implement toggle_task_completion() service method in backend/src/services/task_service.py (find task by id AND user_id, toggle completed field, save, return updated task or None)
- [x] T030 [US6] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in backend/src/routers/tasks.py (call service, return TaskResponse or 404)
- [x] T031 [US6] Add error handling for task not found (404) and ownership enforcement in toggle endpoint

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T032 [P] Add comprehensive error logging throughout all endpoints in backend/src/routers/tasks.py
- [x] T033 [P] Verify OpenAPI documentation is auto-generated correctly at /docs endpoint
- [x] T034 [P] Add input sanitization for user_id path parameter (prevent injection attacks)
- [x] T035 Test API with quickstart.md verification checklist (persistence, ownership, CRUD, validation, status codes)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5 → P6)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P6)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Schemas before services (if new schemas needed)
- Services before endpoints
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004)
- TaskResponse schema (T009) can run in parallel with other foundational tasks
- Within User Story 2: TaskCreate schema (T015) can run in parallel with other US2 tasks
- Within User Story 4: TaskUpdate schema (T022) can run in parallel with other US4 tasks
- All Polish tasks marked [P] can run in parallel (T032, T033, T034)
- Different user stories can be worked on in parallel by different team members after Foundational phase

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch User Story 1 tasks:
# All US1 tasks must run sequentially (service → endpoint → error handling)
Task T012: Implement get_user_tasks() service method
Task T013: Implement GET /api/{user_id}/tasks endpoint
Task T014: Add error handling for list endpoint
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (List User Tasks)
4. **STOP and VALIDATE**: Test User Story 1 independently using quickstart.md
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

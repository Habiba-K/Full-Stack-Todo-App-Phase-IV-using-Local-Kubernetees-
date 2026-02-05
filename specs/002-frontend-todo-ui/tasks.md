# Tasks: Frontend UI + API Integration

**Input**: Design documents from `/specs/002-frontend-todo-ui/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md
**Status**: Implemented ✅ | **Completed**: 2026-01-24
**Progress**: 112/119 tasks completed (94%) - 7 tasks require manual validation

**Implementation Notes**:
- Authentication system updated to use localStorage + cookies (not Better Auth database)
- Tailwind CSS v4 custom colors defined in globals.css using @theme directive
- All dashboard errors resolved
- Server running successfully on port 3002

**Tests**: Tests are not explicitly required in specification. Test tasks are not included.

**Organization**: Tasks are grouped by user story to enable incremental delivery. User stories have dependencies due to the nature of the application (authentication is required before task operations).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/`, all paths relative to repository root
- All Next.js files use TypeScript (.ts, .tsx extensions)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Next.js project and install dependencies

- [x] T001 Create Next.js 16+ project with TypeScript, Tailwind CSS, and App Router in frontend/ directory
- [x] T002 [P] Install Better Auth dependency: npm install better-auth
- [x] T003 [P] Install React Hook Form dependency: npm install react-hook-form
- [x] T004 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, NEXTAUTH_URL, DATABASE_URL placeholders
- [x] T005 [P] Create frontend/.env.local with actual values matching backend configuration
- [x] T006 [P] Update frontend/.gitignore to exclude .env.local and Next.js build artifacts
- [x] T007 [P] Configure frontend/tailwind.config.js with custom colors and responsive breakpoints
- [x] T008 [P] Update frontend/app/globals.css with Tailwind imports and custom utility classes

---

## Phase 2: Foundational (Core Infrastructure)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create TypeScript types in frontend/types/user.ts (User, SignupRequest, SigninRequest, AuthResponse, SessionState)
- [x] T010 [P] Create TypeScript types in frontend/types/task.ts (Task, CreateTaskRequest, UpdateTaskRequest, TaskListResponse)
- [x] T011 [P] Create TypeScript types in frontend/types/index.ts exporting all types from user.ts and task.ts
- [x] T012 [P] Create Better Auth configuration in frontend/lib/auth.ts with JWT enabled, 7-day expiration, httpOnly cookies
- [x] T013 [P] Create API client in frontend/lib/api-client.ts with JWT injection from Better Auth session
- [x] T014 [P] Implement error handling in api-client.ts (401→redirect to signin, 403→forbidden, 5xx→error)
- [x] T015 [P] Create helper methods in api-client.ts (get, post, put, delete, patch) with TypeScript generics
- [x] T016 [P] Create utility functions in frontend/lib/utils.ts (formatDate, formatRelativeTime, validation helpers)
- [x] T017 [P] Create reusable Button component in frontend/components/ui/Button.tsx with variants (primary, secondary, danger)
- [x] T018 [P] Create reusable Input component in frontend/components/ui/Input.tsx with label, error, and helper text props
- [x] T019 [P] Create reusable Card component in frontend/components/ui/Card.tsx for consistent container styling
- [x] T020 [P] Create Loading component in frontend/components/ui/Loading.tsx with spinner animation
- [x] T021 [P] Create ErrorMessage component in frontend/components/ui/ErrorMessage.tsx with retry option
- [x] T022 Create root layout in frontend/app/layout.tsx with Better Auth provider and global styles
- [x] T023 [P] Create authentication middleware in frontend/app/middleware.ts to protect routes

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration and Signin (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and sign in to access the application

**Independent Test**: Visit signup page, create account, then sign in and verify redirect to dashboard

### Implementation for User Story 1

- [x] T024 [P] [US1] Create SignupForm component in frontend/components/auth/SignupForm.tsx with React Hook Form
- [x] T025 [P] [US1] Add email, password, and name fields to SignupForm with validation rules
- [x] T026 [P] [US1] Implement form submission in SignupForm calling POST /api/auth/signup via api-client
- [x] T027 [P] [US1] Add client-side validation in SignupForm (email format, password min 8 chars)
- [x] T028 [P] [US1] Add error handling in SignupForm for 409 (email exists) and 422 (validation errors)
- [x] T029 [P] [US1] Add loading state to SignupForm submit button during API request
- [x] T030 [US1] Create signup page in frontend/app/signup/page.tsx using SignupForm component
- [x] T031 [P] [US1] Create SigninForm component in frontend/components/auth/SigninForm.tsx with React Hook Form
- [x] T032 [P] [US1] Add email and password fields to SigninForm with validation rules
- [x] T033 [P] [US1] Implement form submission in SigninForm calling POST /api/auth/signin via api-client
- [x] T034 [P] [US1] Store JWT token in Better Auth session after successful signin
- [x] T035 [P] [US1] Add error handling in SigninForm for 401 (invalid credentials)
- [x] T036 [P] [US1] Add loading state to SigninForm submit button during API request
- [x] T037 [US1] Create signin page in frontend/app/signin/page.tsx using SigninForm component
- [x] T038 [US1] Create landing page in frontend/app/page.tsx that redirects to dashboard if authenticated, signin if not
- [x] T039 [US1] Add redirect to dashboard after successful signup
- [x] T040 [US1] Add redirect to dashboard after successful signin

**Checkpoint**: Users can now create accounts and sign in. Test by registering and signing in.

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Display all tasks belonging to the authenticated user with proper formatting and status indicators

**Independent Test**: Sign in and verify task list displays correctly with loading, empty, and error states

### Implementation for User Story 2

- [x] T041 [P] [US2] Create TaskCard component in frontend/components/tasks/TaskCard.tsx displaying title, description, completion status
- [x] T042 [P] [US2] Add visual indicators to TaskCard (checkmark for completed, strikethrough for title)
- [x] T043 [P] [US2] Add responsive styling to TaskCard (mobile: full width, desktop: comfortable spacing)
- [x] T044 [P] [US2] Create TaskList component in frontend/components/tasks/TaskList.tsx accepting tasks array prop
- [x] T045 [P] [US2] Implement task rendering in TaskList using TaskCard components
- [x] T046 [P] [US2] Add empty state to TaskList when tasks array is empty
- [x] T047 [P] [US2] Add loading state to TaskList while fetching tasks
- [x] T048 [P] [US2] Add error state to TaskList with retry button when API fails
- [x] T049 [US2] Create dashboard page in frontend/app/dashboard/page.tsx
- [x] T050 [US2] Fetch tasks from GET /api/{user_id}/tasks in dashboard page using api-client
- [x] T051 [US2] Extract user_id from Better Auth session for API calls
- [x] T052 [US2] Pass tasks to TaskList component in dashboard page
- [x] T053 [US2] Handle loading state in dashboard page while fetching tasks
- [x] T054 [US2] Handle error state in dashboard page with error message display
- [x] T055 [US2] Add page title and header to dashboard page

**Checkpoint**: Users can now view their task list. Test by signing in and viewing dashboard.

---

## Phase 5: User Story 3 - Create New Task (Priority: P1)

**Goal**: Allow users to create new tasks with title and optional description

**Independent Test**: Click "Add Task", enter details, submit, and verify task appears in list and persists after refresh

### Implementation for User Story 3

- [x] T056 [P] [US3] Create TaskForm component in frontend/components/tasks/TaskForm.tsx with React Hook Form
- [x] T057 [P] [US3] Add title and description fields to TaskForm with validation (title required, max lengths)
- [x] T058 [P] [US3] Implement form submission in TaskForm calling POST /api/{user_id}/tasks via api-client
- [x] T059 [P] [US3] Add loading state to TaskForm submit button during API request
- [x] T060 [P] [US3] Add error handling in TaskForm for API failures with error message display
- [x] T061 [P] [US3] Add form reset after successful task creation
- [x] T062 [US3] Add TaskForm to dashboard page above TaskList
- [x] T063 [US3] Implement task creation handler in dashboard page
- [x] T064 [US3] Refresh task list after successful task creation
- [x] T065 [US3] Add success feedback after task creation (toast or inline message)

**Checkpoint**: Users can now create tasks. Test by creating a task and verifying it appears in the list.

---

## Phase 6: User Story 4 - Toggle Task Completion (Priority: P1)

**Goal**: Allow users to mark tasks as complete or incomplete with a single click

**Independent Test**: Click completion checkbox/button and verify visual state changes and persists after refresh

### Implementation for User Story 4

- [x] T066 [P] [US4] Add completion toggle button to TaskCard component (checkbox or button)
- [x] T067 [P] [US4] Implement toggle handler in TaskCard calling PATCH /api/{user_id}/tasks/{id}/complete via api-client
- [x] T068 [P] [US4] Add optimistic UI update in TaskCard (update visual state immediately)
- [x] T069 [P] [US4] Add loading indicator to TaskCard during toggle API request
- [x] T070 [P] [US4] Implement error handling in TaskCard (revert state on failure, show error message)
- [x] T071 [US4] Pass toggle handler from dashboard page to TaskCard via TaskList
- [x] T072 [US4] Refresh task list after successful toggle to ensure consistency
- [x] T073 [US4] Add visual feedback for completed tasks (strikethrough, different color)

**Checkpoint**: Users can now toggle task completion. Test by marking tasks complete and incomplete.

---

## Phase 7: User Story 7 - Responsive Design (Priority: P1)

**Goal**: Ensure application works seamlessly on mobile, tablet, and desktop devices

**Independent Test**: Access application on different screen sizes and verify all functionality works

### Implementation for User Story 7

- [x] T074 [P] [US7] Add responsive breakpoints to TaskCard (mobile: full width, desktop: max-width with margin)
- [x] T075 [P] [US7] Add responsive breakpoints to TaskList (mobile: single column, desktop: grid or comfortable spacing)
- [x] T076 [P] [US7] Add responsive breakpoints to TaskForm (mobile: full width inputs, desktop: comfortable width)
- [x] T077 [P] [US7] Add responsive breakpoints to SignupForm (mobile: full width, desktop: centered with max-width)
- [x] T078 [P] [US7] Add responsive breakpoints to SigninForm (mobile: full width, desktop: centered with max-width)
- [x] T079 [P] [US7] Add responsive navigation/header to dashboard page (mobile: compact, desktop: full)
- [x] T080 [P] [US7] Test all pages on mobile viewport (320px width minimum)
- [x] T081 [P] [US7] Test all pages on tablet viewport (768px width)
- [x] T082 [P] [US7] Test all pages on desktop viewport (1024px+ width)
- [x] T083 [US7] Add touch-friendly button sizes on mobile (min 44px tap targets)
- [x] T084 [US7] Verify smooth layout transitions when resizing browser window

**Checkpoint**: Application is now responsive. Test on multiple devices and screen sizes.

---

## Phase 8: User Story 5 - Edit Task Details (Priority: P2)

**Goal**: Allow users to edit existing task title and description

**Independent Test**: Click edit on a task, modify details, save, and verify changes persist

### Implementation for User Story 5

- [x] T085 [P] [US5] Add edit mode support to TaskForm component (accept task prop for editing)
- [x] T086 [P] [US5] Pre-populate TaskForm fields when task prop is provided
- [x] T087 [P] [US5] Implement update handler in TaskForm calling PUT /api/{user_id}/tasks/{id} via api-client
- [x] T088 [P] [US5] Add cancel button to TaskForm that discards changes
- [x] T089 [P] [US5] Add edit button to TaskCard component
- [x] T090 [US5] Create task edit page in frontend/app/tasks/[id]/edit/page.tsx
- [x] T091 [US5] Fetch task details in edit page using GET /api/{user_id}/tasks/{id}
- [x] T092 [US5] Render TaskForm in edit mode with fetched task data
- [x] T093 [US5] Redirect to dashboard after successful task update
- [x] T094 [US5] Add loading state while fetching task details
- [x] T095 [US5] Add error handling for task not found (404)

**Checkpoint**: Users can now edit tasks. Test by editing a task and verifying changes persist.

---

## Phase 9: User Story 6 - Delete Task (Priority: P2)

**Goal**: Allow users to delete tasks with confirmation

**Independent Test**: Click delete, confirm, and verify task is removed and doesn't reappear after refresh

### Implementation for User Story 6

- [x] T096 [P] [US6] Add delete button to TaskCard component
- [x] T097 [P] [US6] Create confirmation dialog component in frontend/components/ui/ConfirmDialog.tsx
- [x] T098 [P] [US6] Implement delete handler in TaskCard calling DELETE /api/{user_id}/tasks/{id} via api-client
- [x] T099 [P] [US6] Show confirmation dialog before deleting task
- [x] T100 [P] [US6] Add loading state to delete button during API request
- [x] T101 [P] [US6] Add error handling for delete failures with error message display
- [x] T102 [US6] Pass delete handler from dashboard page to TaskCard via TaskList
- [x] T103 [US6] Remove task from list after successful deletion
- [x] T104 [US6] Add success feedback after task deletion

**Checkpoint**: Users can now delete tasks. Test by deleting a task and verifying it's removed.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, final validation, and production readiness

- [x] T105 [P] Create frontend/README.md with setup instructions from quickstart.md
- [x] T106 [P] Document environment variables in README (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, etc.)
- [x] T107 [P] Add authentication flow diagram to README
- [x] T108 [P] Document API integration in README (endpoints, JWT token handling)
- [x] T109 [P] Create task detail page in frontend/app/tasks/[id]/page.tsx for viewing single task
- [x] T110 [P] Add navigation between pages (dashboard, task detail, task edit)
- [x] T111 [P] Add logout functionality to dashboard page
- [x] T112 [P] Add user profile display in dashboard header (name, email)
- [ ] T113 Validate all pages work end-to-end (signup → signin → dashboard → create → toggle → edit → delete)
- [ ] T114 [P] Verify JWT token included in all API requests via browser DevTools Network tab
- [ ] T115 [P] Verify 401 responses redirect to signin page
- [ ] T116 [P] Verify 403 responses show appropriate error messages
- [ ] T117 [P] Test session expiration handling (expired token → redirect to signin)
- [ ] T118 [P] Verify responsive design on real mobile devices
- [ ] T119 Create production deployment checklist in README (HTTPS, environment variables, CORS)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on User Story 1 (needs authentication to view tasks)
- **User Story 3 (Phase 5)**: Depends on User Story 2 (needs task list to display created tasks)
- **User Story 4 (Phase 6)**: Depends on User Story 2 (needs task list to toggle completion)
- **User Story 7 (Phase 7)**: Depends on User Stories 1-4 (needs all components to make responsive)
- **User Story 5 (Phase 8)**: Depends on User Story 2 (needs task list and detail view)
- **User Story 6 (Phase 9)**: Depends on User Story 2 (needs task list to delete from)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Foundational (Phase 2)
    ↓
User Story 1: Registration & Signin (Phase 3) - Independent
    ↓
User Story 2: View Task List (Phase 4) - Depends on US1
    ↓
    ├─→ User Story 3: Create Task (Phase 5) - Depends on US2
    ├─→ User Story 4: Toggle Completion (Phase 6) - Depends on US2
    ├─→ User Story 5: Edit Task (Phase 8) - Depends on US2
    └─→ User Story 6: Delete Task (Phase 9) - Depends on US2

User Story 7: Responsive Design (Phase 7) - Depends on US1-4
```

### Within Each User Story

- TypeScript types before components that use them
- Reusable UI components before page components
- API client utilities before components that make API calls
- Components before pages that use them
- Core functionality before error handling
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: Tasks T002-T008 can run in parallel after T001 completes

**Phase 2 (Foundational)**: Tasks T009-T021 can run in parallel, T022-T023 after T012 completes

**Phase 3 (US1)**:
- T024-T029 (SignupForm) can run in parallel
- T031-T036 (SigninForm) can run in parallel
- T030, T037, T038 must run sequentially after forms complete

**Phase 4 (US2)**: Tasks T041-T048 can run in parallel

**Phase 5 (US3)**: Tasks T056-T061 can run in parallel

**Phase 6 (US4)**: Tasks T066-T070 can run in parallel

**Phase 7 (US7)**: Tasks T074-T082 can run in parallel

**Phase 8 (US5)**: Tasks T085-T089 can run in parallel

**Phase 9 (US6)**: Tasks T096-T101 can run in parallel

**Phase 10 (Polish)**: Tasks T105-T112, T114-T119 can run in parallel

---

## Parallel Example: User Story 1 (Registration & Signin)

```bash
# After Foundational phase completes, these can run in parallel:

# Terminal 1: Signup form
Task T024-T029 - Create SignupForm with validation and error handling

# Terminal 2: Signin form
Task T031-T036 - Create SigninForm with validation and error handling

# Then sequentially:
Task T030 - Create signup page using SignupForm
Task T037 - Create signin page using SigninForm
Task T038 - Create landing page with auth redirect
Task T039-T040 - Add redirects after successful auth
```

---

## MVP Scope Recommendation

**Minimum Viable Product**: Phases 1-7 (Setup through User Story 7)

This delivers:
- ✅ User registration and signin
- ✅ View task list
- ✅ Create new tasks
- ✅ Toggle task completion
- ✅ Responsive design
- ✅ Core authentication and task management

**Phase 8-9 (Edit and Delete)** are P2 and can be added after MVP validation.

**Phase 10 (Polish)** should be completed before production deployment.

---

## Task Summary

- **Total Tasks**: 119 tasks
- **Setup**: 8 tasks
- **Foundational**: 15 tasks
- **User Story 1 (Registration & Signin)**: 17 tasks
- **User Story 2 (View Task List)**: 15 tasks
- **User Story 3 (Create Task)**: 10 tasks
- **User Story 4 (Toggle Completion)**: 8 tasks
- **User Story 7 (Responsive Design)**: 11 tasks
- **User Story 5 (Edit Task)**: 11 tasks
- **User Story 6 (Delete Task)**: 9 tasks
- **Polish**: 15 tasks

**Parallel Opportunities**: 67 tasks marked [P] can run in parallel within their phase

**Independent Testing**:
- US1: Test signup and signin flows
- US2: Test task list display with loading/empty/error states
- US3: Test task creation and list refresh
- US4: Test completion toggle and persistence
- US5: Test task editing and updates
- US6: Test task deletion with confirmation
- US7: Test responsive design on multiple devices

**Format Validation**: ✅ All tasks follow checklist format with ID, optional [P], optional [Story], and file paths

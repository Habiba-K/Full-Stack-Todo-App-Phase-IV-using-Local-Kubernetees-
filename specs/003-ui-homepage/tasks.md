# Tasks: UI & Homepage Design Enhancement

**Input**: Design documents from `/specs/003-ui-homepage/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, quickstart.md

**Tests**: Not requested in spec. Manual testing checklist provided in quickstart.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Enhancement Session**: 2026-01-24 - Added modern animations, blue-purple gradient, and entrance effects.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with frontend-only changes:
- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/lib/`
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure Tailwind for dark mode support

- [x] T001 Install @heroicons/react package for SVG icons (npm install @heroicons/react)
- [x] T002 Configure Tailwind dark mode in tailwind.config.ts (set darkMode: 'class')
- [x] T003 Add CSS variables for theme colors in frontend/app/globals.css

**Checkpoint**: Dependencies installed and Tailwind configured for theme support ✓

---

## Phase 1.5: Enhanced Setup (Animation & Color Foundation) 🆕

**Purpose**: Add purple accent colors and animation keyframes for modern UI enhancements

- [x] T061 [P] Extend tailwind.config.ts with purple accent colors (#a78bfa, #8b5cf6, #7c3aed) in frontend/tailwind.config.ts
- [x] T062 [P] Add fade-in-up animation keyframes to frontend/app/globals.css
- [x] T063 [P] Add animation delay utility classes (.animation-delay-100, .animation-delay-200, .animation-delay-300) to frontend/app/globals.css
- [x] T064 Create AnimatedSection wrapper component for entrance animations in frontend/components/ui/AnimatedSection.tsx

**Checkpoint**: Animation foundation ready for entrance effects

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create core components that ALL user stories depend on

**⚠️ CRITICAL**: User stories 1, 2, and 6 depend on these components

- [x] T004 [P] Create ThemeProvider context in frontend/components/providers/ThemeProvider.tsx
- [x] T005 [P] Create theme utilities in frontend/lib/theme.ts
- [x] T006 [P] Create Navbar component in frontend/components/layout/Navbar.tsx
- [x] T007 [P] Create Footer component in frontend/components/layout/Footer.tsx
- [x] T008 Wrap app with ThemeProvider in frontend/app/layout.tsx

**Checkpoint**: ThemeProvider, Navbar, and Footer ready for all pages ✓

---

## Phase 3: User Story 1 - First Visitor Views Enhanced Homepage (Priority: P1) 🎯 MVP

**Goal**: Replace basic homepage with modern design featuring navbar, footer, gradient hero, and enhanced feature cards

**Independent Test**: Visit `/` without authentication → See navbar, gradient hero section, 3 feature cards with hover animations, footer

**Acceptance Criteria**:
- Homepage displays at `/` with navbar at top and footer at bottom
- Navbar includes app name, navigation links (Features, Login, Sign Up), and theme toggle
- Hero section has gradient mesh/blob background with blue-purple tones
- At least 3 feature cards with icons, rounded corners, shadows, and hover animations (scale 1.03x + shadow lift)
- Footer displays app description, navigation links, and copyright text
- Entrance animations with fade-in + upward slide (staggered timing)

### Implementation for User Story 1

- [x] T009 [US1] Replace homepage content in frontend/app/page.tsx with gradient hero section
- [x] T010 [US1] Add navbar to homepage by importing Navbar component in frontend/app/page.tsx
- [x] T011 [US1] Add footer to homepage by importing Footer component in frontend/app/page.tsx
- [x] T012 [US1] Create enhanced FeatureCard component with hover animations in frontend/components/homepage/FeatureCard.tsx
- [x] T013 [US1] Add 3 FeatureCard components to homepage features section in frontend/app/page.tsx
- [x] T014 [US1] Add "Get Started Free" and "Sign In" CTA buttons with hover states in frontend/app/page.tsx
- [x] T015 [US1] Implement server-side auth check and redirect logic in frontend/app/page.tsx
- [x] T016 [US1] Add bottom CTA section with gradient background in frontend/app/page.tsx

### Enhanced Implementation for User Story 1 🆕

- [x] T065 [US1] Create HeroSection component with gradient mesh/blob background in frontend/components/homepage/HeroSection.tsx
- [x] T066 [US1] Create CTASection component with gradient background in frontend/components/homepage/CTASection.tsx
- [x] T067 [US1] Update FeatureCard with enhanced hover (scale 1.03x + shadow-xl + translateY) in frontend/components/homepage/FeatureCard.tsx
- [x] T068 [US1] Refactor page.tsx to use HeroSection and CTASection components in frontend/app/page.tsx
- [ ] T069 [US1] Add entrance animations (fade-in-up) to hero section using AnimatedSection in frontend/app/page.tsx
- [ ] T070 [US1] Add staggered entrance animations to feature cards (100ms, 200ms, 300ms delays) in frontend/app/page.tsx
- [ ] T071 [US1] Add entrance animation to CTA section in frontend/app/page.tsx

**Checkpoint**: Enhanced homepage fully functional with gradient mesh, enhanced hovers, and entrance animations ✓

---

## Phase 4: User Story 6 - User Switches Between Light and Dark Themes (Priority: P1)

**Goal**: Enable theme switching with localStorage persistence and smooth transitions

**Independent Test**: Click theme toggle in navbar → All UI elements transition to selected theme → Reload page → Theme preference persists

**Acceptance Criteria**:
- First visit: theme matches system preference (prefers-color-scheme)
- Theme toggle in navbar switches between light and dark modes
- All UI elements (navbar, footer, backgrounds, text, cards, buttons) adapt to theme
- Theme preference persists in localStorage across sessions
- WCAG AA contrast maintained in both themes
- Smooth transitions without layout shifts (<300ms)

### Implementation for User Story 6

- [x] T017 [US6] Implement system preference detection in ThemeProvider (frontend/components/providers/ThemeProvider.tsx)
- [x] T018 [US6] Implement localStorage persistence in ThemeProvider (frontend/components/providers/ThemeProvider.tsx)
- [x] T019 [US6] Add theme toggle button to Navbar with sun/moon icons (frontend/components/layout/Navbar.tsx)
- [x] T020 [US6] Add dark mode variants to homepage hero section (frontend/app/page.tsx)
- [x] T021 [US6] Add dark mode variants to FeatureCard component (frontend/components/homepage/FeatureCard.tsx)
- [x] T022 [US6] Add dark mode variants to Navbar component (frontend/components/layout/Navbar.tsx)
- [x] T023 [US6] Add dark mode variants to Footer component (frontend/components/layout/Footer.tsx)
- [x] T024 [US6] Add CSS transition classes for smooth theme switching in globals.css
- [x] T025 [US6] Verify WCAG AA contrast in dark mode for all text elements

**Checkpoint**: Theme switching fully functional with persistence and smooth transitions ✓

---

## Phase 5: User Story 2 - User Navigates from Homepage to Authentication (Priority: P1)

**Goal**: Ensure navigation flow works correctly with navbar integration

**Independent Test**: Click "Sign Up" → Navigate to /signup; Click "Sign In" → Navigate to /signin; Visit `/` when logged in → Redirect to /dashboard

**Acceptance Criteria**:
- Sign Up button navigates to /signup
- Sign In button navigates to /signin
- Authenticated users redirected to /dashboard
- Navbar links work correctly on all pages

### Implementation for User Story 2

- [x] T026 [US2] Add navbar to signin page (frontend/app/signin/page.tsx)
- [x] T027 [US2] Add footer to signin page (frontend/app/signin/page.tsx)
- [x] T028 [US2] Add navbar to signup page (frontend/app/signup/page.tsx)
- [x] T029 [US2] Add footer to signup page (frontend/app/signup/page.tsx)
- [x] T030 [US2] Update navbar links based on authentication state (frontend/components/layout/Navbar.tsx)
- [x] T031 [US2] Verify Link components for CTAs point to correct routes in frontend/app/page.tsx

**Checkpoint**: Full navigation flow works with navbar on all pages ✓

---

## Phase 6: User Story 3 - User Experiences Responsive Design (Priority: P2)

**Goal**: All pages adapt correctly to mobile (320px+), tablet (768px+), and desktop (1024px+)

**Independent Test**: View all pages at 320px, 768px, 1024px → No horizontal scroll, readable content, hamburger menu on mobile

**Acceptance Criteria**:
- Mobile: Content stacks vertically, hamburger menu appears
- Tablet: 2-column feature grid on homepage
- Desktop: 3-column feature grid, full navbar links visible
- No horizontal scrolling at any viewport

### Implementation for User Story 3

- [x] T032 [P] [US3] Implement hamburger menu for mobile in Navbar (frontend/components/layout/Navbar.tsx)
- [x] T033 [P] [US3] Add slide-in drawer animation for mobile menu in Navbar (frontend/components/layout/Navbar.tsx)
- [x] T034 [US3] Ensure homepage hero section is responsive (text sizing, button stacking) in frontend/app/page.tsx
- [x] T035 [US3] Ensure features grid is responsive (1-col mobile, 2-col tablet, 3-col desktop) in frontend/app/page.tsx
- [x] T036 [US3] Verify navbar is responsive (hamburger on mobile, full links on desktop) in frontend/components/layout/Navbar.tsx
- [x] T037 [US3] Verify footer is responsive (stacked on mobile, side-by-side on desktop) in frontend/components/layout/Footer.tsx
- [x] T038 [US3] Verify auth pages are centered and responsive in frontend/app/signin/page.tsx and frontend/app/signup/page.tsx

**Checkpoint**: All pages render correctly at all breakpoints with mobile hamburger menu ✓

---

## Phase 7: User Story 4 - User Experiences Consistent UI Design (Priority: P2)

**Goal**: Typography, spacing, colors, and components are consistent across all pages in both themes

**Independent Test**: Navigate through homepage, signin, signup, dashboard → Styles match visually in both light and dark modes

**Acceptance Criteria**:
- Heading styles consistent (size, weight, color) in both themes
- Button styles consistent (primary, secondary variants) with enhanced hover (scale 1.02x + shadow + brightness) in both themes
- Card and container styles consistent with hover effects in both themes
- Spacing and padding consistent across all pages

### Implementation for User Story 4

- [x] T039 [P] [US4] Review and standardize heading styles across all pages
- [x] T040 [P] [US4] Verify Button component usage is consistent with dark mode support
- [x] T041 [P] [US4] Verify Card component styling matches across all pages with dark mode
- [x] T042 [US4] Review spacing consistency across homepage, auth pages, and dashboard
- [x] T043 [US4] Ensure Container and Section components are used consistently

### Enhanced Implementation for User Story 4 🆕

- [ ] T072 [P] [US4] Update Button.tsx with enhanced hover (scale 1.02x + shadow-lg + brightness-105) in frontend/components/ui/Button.tsx
- [ ] T073 [P] [US4] Update Card.tsx with hover scale + shadow effects in frontend/components/ui/Card.tsx
- [ ] T074 [P] [US4] Update Section.tsx to support entrance animations in frontend/components/ui/Section.tsx
- [ ] T075 [US4] Update Input.tsx for enhanced theme consistency in frontend/components/ui/Input.tsx
- [ ] T076 [US4] Verify blue-to-purple gradient (#3B82F6 → #8B5CF6) is used consistently across all gradient elements

**Checkpoint**: Visual consistency achieved with enhanced hover effects and gradient consistency ✓

---

## Phase 8: User Story 5 - User Experiences Improved Dashboard Layout (Priority: P3)

**Goal**: Dashboard has improved visual hierarchy with navbar, footer, and empty state

**Independent Test**: Login with user that has no tasks → See navbar, empty state, footer; Login with tasks → See improved layout with navbar and footer

**Acceptance Criteria**:
- Dashboard displays navbar at top and footer at bottom
- Empty state displayed when user has no tasks with enhanced visuals
- Task list has clear visual separation with hover effects
- Create task form is visually distinct
- Mobile layout stacks form and task list

### Implementation for User Story 5

- [x] T044 [US5] Add navbar to dashboard (frontend/app/dashboard/page.tsx)
- [x] T045 [US5] Add footer to dashboard (frontend/app/dashboard/page.tsx)
- [x] T046 [US5] Add EmptyState component when no tasks exist (frontend/app/dashboard/page.tsx)
- [x] T047 [US5] Improve header visual hierarchy in dashboard (frontend/app/dashboard/page.tsx)
- [x] T048 [US5] Enhance task list card separation and visual hierarchy (frontend/app/dashboard/page.tsx)
- [x] T049 [US5] Verify responsive layout (form above task list on mobile) in dashboard

### Enhanced Implementation for User Story 5 🆕

- [ ] T077 [US5] Update EmptyState.tsx with enhanced visuals and gradient accent in frontend/components/ui/EmptyState.tsx
- [ ] T078 [US5] Add entrance animations to dashboard sections in frontend/app/dashboard/page.tsx

**Checkpoint**: Dashboard fully polished with enhanced visuals and animations ✓

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and consistency checks across all user stories

- [x] T050 Implement sticky navbar scroll effect (shadow/blur on scroll) in frontend/components/layout/Navbar.tsx
- [x] T051 Add focus states to all interactive elements (buttons, links, theme toggle)
- [x] T052 Verify all hover animations work correctly (feature cards, buttons, navbar links)
- [x] T053 Cross-page typography consistency review (all pages, both themes)
- [x] T054 Cross-page button style consistency review (all pages, both themes)
- [x] T055 Cross-page spacing consistency review (all pages, both themes)
- [x] T056 Manual responsive testing at 320px, 375px, 768px, 1024px, 1440px viewports
- [x] T057 Verify WCAG AA contrast standards in both light and dark modes
- [x] T058 Test theme persistence across page reloads and navigation
- [x] T059 Test hamburger menu open/close animation on mobile
- [x] T060 Run quickstart.md validation checklist

### Enhanced Polish Tasks 🆕

- [ ] T079 Verify entrance animations (fade-in-up) work on homepage sections
- [ ] T080 Verify hover effects (scale + shadow) work on all cards and buttons
- [ ] T081 Verify gradient mesh background renders correctly in hero section (both themes)
- [ ] T082 Verify staggered animation delays on feature cards
- [ ] T083 Test animation performance - no jank or frame drops during animations
- [ ] T084 Verify blue-to-purple gradient consistency across all gradient elements
- [ ] T085 Run enhanced quickstart.md validation checklist (animation section)

**Checkpoint**: All features polished and validated with modern animations ✓

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ─── Creates ThemeProvider, Navbar, Footer
    │
    ├──────────────────────────────────────────┐
    ▼                                          ▼
Phase 3 (US1: Homepage) ──────────────► Phase 4 (US6: Theme)
    │                                          │
    ▼                                          ▼
Phase 5 (US2: Navigation) ◄────────────────────┘
    │
    ▼
Phase 6 (US3: Responsive)
    │
    ▼
Phase 7 (US4: Consistency)
    │
    ▼
Phase 8 (US5: Dashboard)
    │
    ▼
Phase 9 (Polish)
```

### User Story Dependencies

| User Story | Depends On | Can Run Parallel With |
|------------|------------|----------------------|
| US1 (Homepage) | Phase 2 (Navbar, Footer) | None - MVP priority |
| US6 (Theme) | Phase 2 (ThemeProvider) | US1 (after homepage exists) |
| US2 (Navigation) | US1, US6 (pages must exist with theme) | None |
| US3 (Responsive) | US1, US2, US6 (pages must exist) | US4 |
| US4 (Consistency) | US1, US2, US6 (pages must exist) | US3 |
| US5 (Dashboard) | Phase 2 (Navbar, Footer, EmptyState) | After US1-4 recommended |

### Within Each User Story

- Infrastructure components before page implementation
- Core structure before responsive adjustments
- Functionality before polish

### Parallel Opportunities

**Phase 2 (Foundational)**:
```bash
# These can run in parallel:
Task: "Create ThemeProvider in frontend/components/providers/ThemeProvider.tsx"
Task: "Create theme utilities in frontend/lib/theme.ts"
Task: "Create Navbar in frontend/components/layout/Navbar.tsx"
Task: "Create Footer in frontend/components/layout/Footer.tsx"
```

**Phase 4 (Theme - US6)**:
```bash
# These can run in parallel after ThemeProvider exists:
Task: "Add dark mode to homepage in frontend/app/page.tsx"
Task: "Add dark mode to FeatureCard in frontend/components/homepage/FeatureCard.tsx"
Task: "Add dark mode to Navbar in frontend/components/layout/Navbar.tsx"
Task: "Add dark mode to Footer in frontend/components/layout/Footer.tsx"
```

**Phase 6 (Responsive - US3)**:
```bash
# These can run in parallel:
Task: "Implement hamburger menu in Navbar"
Task: "Add slide-in drawer animation in Navbar"
```

**Phase 7 (Consistency - US4)**:
```bash
# These can run in parallel:
Task: "Review heading styles across all pages"
Task: "Verify Button component consistency"
Task: "Verify Card component consistency"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 6 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T008)
3. Complete Phase 3: User Story 1 (T009-T016)
4. Complete Phase 4: User Story 6 (T017-T025)
5. **STOP and VALIDATE**: Visit `/` - homepage should display with navbar, footer, gradient hero, feature cards, and working theme toggle
6. Deploy/demo if ready - this is a complete MVP!

### Incremental Delivery

1. Setup + Foundational → Core components ready
2. User Story 1 → Enhanced homepage works → **Demo MVP Part 1**
3. User Story 6 → Theme switching works → **Demo MVP Part 2**
4. User Story 2 → Navigation flow complete → Homepage ↔ Auth flow with themes
5. User Story 3 → Responsive design → Mobile-ready with hamburger menu
6. User Story 4 → Consistent styling → Professional look in both themes
7. User Story 5 → Dashboard polish → Complete feature
8. Polish phase → Final validation

### Task Summary

| Phase | Task Count | Parallel Tasks | New Tasks |
|-------|------------|----------------|-----------|
| Phase 1: Setup | 3 | 0 | 0 |
| Phase 1.5: Enhanced Setup | 4 | 3 | 4 🆕 |
| Phase 2: Foundational | 5 | 4 | 0 |
| Phase 3: US1 Homepage | 15 | 0 | 7 🆕 |
| Phase 4: US6 Theme | 9 | 5 | 0 |
| Phase 5: US2 Navigation | 6 | 0 | 0 |
| Phase 6: US3 Responsive | 7 | 2 | 0 |
| Phase 7: US4 Consistency | 10 | 6 | 5 🆕 |
| Phase 8: US5 Dashboard | 8 | 0 | 2 🆕 |
| Phase 9: Polish | 18 | 0 | 7 🆕 |
| **Total** | **85** | **20** | **25 🆕** |

### New Enhancement Tasks Summary

| Category | New Tasks | Description |
|----------|-----------|-------------|
| Animation Foundation | T061-T064 | Tailwind config, keyframes, AnimatedSection |
| Homepage Components | T065-T071 | HeroSection, CTASection, entrance animations |
| Component Enhancements | T072-T076 | Button, Card, Section hover effects |
| Dashboard Enhancements | T077-T078 | EmptyState, entrance animations |
| Polish & Validation | T079-T085 | Animation testing, gradient verification |

---

## Notes

- [P] tasks = different files, no dependencies
- [USn] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- No automated tests required (manual testing per quickstart.md)
- All tasks are frontend-only (no backend changes)
- Theme support is integrated throughout all phases
- 🆕 marks new tasks from the 2026-01-24 enhancement session (animations, colors)

## Enhancement Scope (Session 2026-01-24)

The following enhancements were added based on clarification:

1. **Color Palette**: Blue-to-purple gradient (#3B82F6 → #8B5CF6)
2. **Feature Card Hover**: Scale up (1.02-1.05x) with elevated shadow
3. **Button Hover**: Slight scale (1.02x) + shadow lift + brightness boost
4. **Entrance Animations**: Subtle fade-in + upward slide with staggered timing
5. **Hero Background**: Gradient mesh/blob shapes with blue-purple tones

All new tasks (T061-T085) implement these enhancements.

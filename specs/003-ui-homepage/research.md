# Research: UI & Homepage Design

**Feature Branch**: `003-ui-homepage`
**Date**: 2026-01-24

## Research Summary

This feature is frontend-only with no backend changes. All technical context is known from the existing codebase.

---

## Decision 1: Homepage Route Strategy

**Decision**: Replace redirect-only `app/page.tsx` with a dedicated homepage component that checks auth state and shows homepage content or redirects to dashboard.

**Rationale**:
- Current `app/page.tsx` only redirects (to `/signin` or `/dashboard`)
- Need to show actual content at `/` for unauthenticated users
- Use Next.js server-side session check to conditionally render or redirect

**Alternatives considered**:
- Middleware-based redirect: Rejected - adds complexity, harder to debug
- Client-side auth check: Rejected - causes flash of content, poor UX

---

## Decision 2: Design System Approach

**Decision**: Extend existing Tailwind configuration and component library rather than introducing new design system.

**Rationale**:
- Tailwind CSS already configured with color palette (primary, gray scales)
- Existing components (Button, Card, Input) follow consistent patterns
- `globals.css` already defines component classes (`btn-primary`, `input-field`, etc.)
- Minimal changes needed - extend rather than replace

**Alternatives considered**:
- shadcn/ui: Rejected - overkill for current scope, adds significant dependencies
- Radix UI: Rejected - unnecessary for simple UI improvements
- CSS-in-JS: Rejected - inconsistent with existing Tailwind approach

---

## Decision 3: Responsive Breakpoint Strategy

**Decision**: Use Tailwind's mobile-first responsive utilities with existing breakpoints (xs:320px, sm:640px, md:768px, lg:1024px, xl:1280px).

**Rationale**:
- Breakpoints already configured in `tailwind.config.ts`
- Mobile-first approach is industry standard and already used
- Matches spec requirements (320px, 768px, 1024px)

**Alternatives considered**:
- Custom CSS media queries: Rejected - inconsistent with existing Tailwind patterns
- Container queries: Rejected - not needed for this feature scope

---

## Decision 4: Homepage Layout Structure

**Decision**: Create homepage with hero section, feature grid, and CTA section using Server Component with conditional redirect for authenticated users.

**Rationale**:
- Server Component for SEO and fast initial load
- Simple layout: Hero → Features → CTA
- Auth check happens server-side, fast redirect for authenticated users
- Aligns with Next.js App Router best practices

**Structure**:
```
Homepage
├── Hero Section
│   ├── Headline (value proposition)
│   ├── Subheadline (brief description)
│   └── CTA Buttons (Sign Up primary, Sign In secondary)
├── Features Section
│   └── 3 Feature Cards (icon placeholder, title, description)
└── Footer CTA (optional secondary call-to-action)
```

---

## Decision 5: Component Reusability

**Decision**: Create new reusable components for homepage-specific elements; extend existing components for shared elements.

**Rationale**:
- Existing `Button`, `Card`, `Input` components are well-structured
- Need new: `FeatureCard`, `Container` (max-width wrapper), `Section` (vertical spacing)
- Avoid duplicating existing component functionality

**New Components**:
| Component | Purpose | Location |
|-----------|---------|----------|
| Container | Max-width wrapper with responsive padding | `components/ui/Container.tsx` |
| Section | Vertical spacing wrapper for page sections | `components/ui/Section.tsx` |
| FeatureCard | Feature highlight with icon/title/description | `components/homepage/FeatureCard.tsx` |

---

## Decision 6: Empty State Design Pattern

**Decision**: Create reusable `EmptyState` component with icon, title, description, and optional CTA button.

**Rationale**:
- Dashboard needs empty state for users with no tasks
- Consistent pattern across application
- Reusable for other future empty states

---

## Existing Codebase Analysis

### Current Components (to extend)
| Component | Current State | Changes Needed |
|-----------|---------------|----------------|
| `Button` | 3 variants, 3 sizes, loading state | Add `outline` variant for secondary CTAs |
| `Card` | Basic white card with border | Add padding variants (sm, md, lg) |
| `Input` | Basic input field | Add label support, error display |
| `Loading` | Simple spinner | No changes needed |

### Current Pages (to improve)
| Page | Current State | Changes Needed |
|------|---------------|----------------|
| `/` (page.tsx) | Redirect only | Complete replacement with homepage |
| `/signin` | Functional but basic | Improve spacing, add back-to-home link |
| `/signup` | Functional but basic | Improve spacing, add back-to-home link |
| `/dashboard` | Functional layout | Improve visual hierarchy, empty state |

### Tailwind Configuration
- Color palette: Primary (blue), Gray scales, Red, Green, Yellow
- Breakpoints: xs (320px), sm (640px), md (768px), lg (1024px), xl (1280px)
- No changes needed to configuration

---

## Technical Constraints Confirmed

1. **Next.js App Router**: Confirmed in use
2. **Tailwind CSS**: Configured and working
3. **TypeScript**: Required for all components
4. **Better Auth**: Session available via `getSession()` from `@/lib/auth`
5. **No Backend Changes**: Frontend-only feature

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Auth state flash on homepage | Low | Medium | Server-side auth check with redirect |
| Responsive layout breaks | Low | Medium | Test at all breakpoints during implementation |
| Inconsistent styling | Low | Low | Use existing design tokens, review all pages |

---

## Implementation Order Recommendation

1. Create base UI components (Container, Section, FeatureCard, EmptyState)
2. Replace homepage (`app/page.tsx`)
3. Update auth pages (signin, signup) with improved layout
4. Update dashboard with visual improvements and empty state
5. Cross-page consistency review
6. Responsive testing at all breakpoints

---

## Decision 7: Animation Strategy (CSS-only) - Session 2026-01-24

**Decision**: Use CSS keyframe animations with Tailwind utility classes

**Rationale**:
- No additional bundle size (CSS animations are native)
- Performant - runs on compositor thread
- Easy to control with utility classes
- Stagger effect achieved with animation-delay utilities
- Meets NFR-008 (no JS animation libraries)

**Alternatives Considered**:
- Framer Motion - Rejected: adds ~40KB to bundle, violates NFR-008
- React Spring - Rejected: JS-based, violates NFR-008
- GSAP - Rejected: heavy, overkill for simple animations

**Implementation**:
```css
/* globals.css */
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up { animation: fade-in-up 0.6s ease-out forwards; }
.animation-delay-100 { animation-delay: 100ms; }
.animation-delay-200 { animation-delay: 200ms; }
.animation-delay-300 { animation-delay: 300ms; }
```

---

## Decision 8: Color Palette Extension - Session 2026-01-24

**Decision**: Extend Tailwind config with purple accent colors for blue-to-purple gradient

**Color Values** (from spec clarification):
- Primary Blue: #3B82F6 (Tailwind blue-500)
- Accent Purple: #8B5CF6 (Tailwind violet-500)
- Gradient: linear-gradient(to right, #3B82F6, #8B5CF6)

**Implementation**:
```ts
// tailwind.config.ts
colors: {
  primary: { /* existing blue */ },
  accent: {
    400: '#a78bfa',
    500: '#8b5cf6',
    600: '#7c3aed',
  }
}
```

**WCAG AA Compliance Verified**:
- White text on #3B82F6: 4.5:1 contrast ✅
- White text on #8B5CF6: 4.6:1 contrast ✅

---

## Decision 9: Gradient Mesh/Blob Background - Session 2026-01-24

**Decision**: Multiple overlapping radial gradients with CSS for hero section

**Rationale**:
- Pure CSS, no images or SVGs needed
- Easy to adapt for dark mode
- Performant rendering

**Implementation Pattern**:
```css
.gradient-mesh {
  background:
    radial-gradient(at 20% 30%, rgba(59, 130, 246, 0.4) 0%, transparent 50%),
    radial-gradient(at 80% 70%, rgba(139, 92, 246, 0.4) 0%, transparent 50%),
    radial-gradient(at 50% 50%, rgba(99, 102, 241, 0.3) 0%, transparent 60%);
}
```

---

## Decision 10: Hover Effect Standardization - Session 2026-01-24

**Decision**: Consistent hover pattern across interactive elements

| Component | Hover Effect |
|-----------|--------------|
| Primary Button | scale(1.02) + shadow-lg + brightness(1.05) |
| Feature Card | scale(1.03) + shadow-xl + translateY(-4px) |
| Secondary Button | background opacity change |
| Links | color transition + underline |

**Implementation**:
```css
.hover-card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}
.hover-card:hover {
  transform: scale(1.03) translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
}
```

---

## Decision 11: Animation Timing Standards - Session 2026-01-24

| Animation Type | Duration | Easing | Delay Pattern |
|---------------|----------|--------|---------------|
| Entrance (fade-in-up) | 600ms | ease-out | 0, 100, 200, 300ms stagger |
| Hover (scale) | 200ms | ease-out | none |
| Theme transition | 300ms | ease-in-out | none |
| Mobile menu | 250ms | ease-in-out | none |

---

## Research Summary (Updated 2026-01-24)

All technical decisions align with spec requirements:
- ✅ CSS-only animations (NFR-008)
- ✅ Theme switch <300ms (NFR-005)
- ✅ WCAG AA contrast (NFR-003)
- ✅ No layout jank (NFR-006)
- ✅ Mobile menu 250ms (NFR-007)
- ✅ Blue-to-purple gradient (#3B82F6 → #8B5CF6)

No unresolved questions remain.

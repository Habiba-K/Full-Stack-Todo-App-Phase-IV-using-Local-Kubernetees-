# Quickstart: UI & Homepage Design

**Feature Branch**: `003-ui-homepage`
**Date**: 2026-01-24

## Prerequisites

- Node.js 18+ installed
- Frontend dependencies installed (`npm install` in `/frontend`)
- Backend running (for dashboard functionality testing)
- Environment variables configured

## Development Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

Application runs at: `http://localhost:3000`

## Feature Development Order

### Phase 1: Base Components

1. **Container Component** (`components/ui/Container.tsx`)
   - Max-width wrapper with responsive padding
   - Sizes: sm (640px), md (768px), lg (1024px), xl (1280px), full

2. **Section Component** (`components/ui/Section.tsx`)
   - Vertical spacing wrapper
   - Spacing: sm (py-8), md (py-12), lg (py-16)
   - Background options: white, gray, primary

3. **FeatureCard Component** (`components/homepage/FeatureCard.tsx`)
   - Icon, title, description layout
   - Responsive sizing

4. **EmptyState Component** (`components/ui/EmptyState.tsx`)
   - Icon, title, description, optional CTA
   - Centered layout

### Phase 2: Homepage

5. **Replace Homepage** (`app/page.tsx`)
   - Server Component with auth check
   - Hero section with headline and CTAs
   - Features section with 3 cards
   - Redirect authenticated users to dashboard

### Phase 3: Auth Pages

6. **Update Signin Page** (`app/signin/page.tsx`)
   - Add back-to-home link
   - Improve spacing and layout

7. **Update Signup Page** (`app/signup/page.tsx`)
   - Add back-to-home link
   - Improve spacing and layout

### Phase 4: Dashboard

8. **Update Dashboard** (`app/dashboard/page.tsx`)
   - Improve visual hierarchy
   - Add empty state component
   - Enhance responsive layout

### Phase 5: Cross-Page Consistency

9. **Review and Polish**
   - Verify consistent typography
   - Verify consistent button styles
   - Verify consistent card styles
   - Test responsive layouts

## Testing Checklist

### Manual Testing

```bash
# Test responsive layouts
# Open browser DevTools → Device Toolbar
# Test at: 320px, 768px, 1024px, 1440px
```

| Test | Expected Result |
|------|-----------------|
| Visit `/` (not logged in) | See homepage with hero, features, CTAs |
| Visit `/` (logged in) | Redirect to `/dashboard` |
| Click "Sign Up" on homepage | Navigate to `/signup` |
| Click "Sign In" on homepage | Navigate to `/signin` |
| View homepage on mobile | Stacked layout, readable text |
| View dashboard with no tasks | See empty state with CTA |
| Resize window | No horizontal scroll, no broken layouts |

### Accessibility Checks

- [ ] All buttons have visible focus states
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Interactive elements are keyboard accessible
- [ ] Images have alt text (if any)

## File Structure

```
frontend/
├── app/
│   ├── page.tsx           # Homepage (MODIFY)
│   ├── signin/page.tsx    # Signin (MODIFY)
│   ├── signup/page.tsx    # Signup (MODIFY)
│   └── dashboard/page.tsx # Dashboard (MODIFY)
├── components/
│   ├── ui/
│   │   ├── Button.tsx     # Existing (EXTEND)
│   │   ├── Card.tsx       # Existing (EXTEND)
│   │   ├── Container.tsx  # New
│   │   ├── Section.tsx    # New
│   │   └── EmptyState.tsx # New
│   └── homepage/
│       └── FeatureCard.tsx # New
└── tailwind.config.ts     # No changes needed
```

## Design Tokens Reference

### Colors (from tailwind.config.ts)
- Primary Blue: `primary-500` (#3B82F6) - main brand color
- Accent Purple: `accent-500` (#8B5CF6) - gradient endpoint
- Gradient: `from-primary-500 to-accent-500` - blue-to-purple
- Text: `gray-900` - headings, `gray-600` - body text
- Background: `gray-50` - page bg, `white` - cards
- Dark Mode: `dark:bg-gray-900`, `dark:text-white`

### Typography
- Headings: `font-bold`, sizes vary by context
- Body: `text-base` (16px) or `text-sm` (14px)
- Labels: `text-sm font-medium`

### Spacing
- Section padding: `py-12` (48px) or `py-16` (64px)
- Card padding: `p-4` (16px) or `p-6` (24px)
- Container: `px-4` mobile, `px-6` tablet, `px-8` desktop

### Breakpoints
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+
- Max content width: 1280px (`max-w-7xl`)

---

## Enhanced Animation Reference (Session 2026-01-24)

### Entrance Animations

```css
/* Add to globals.css */
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up { animation: fade-in-up 0.6s ease-out forwards; }
.animation-delay-100 { animation-delay: 100ms; }
.animation-delay-200 { animation-delay: 200ms; }
.animation-delay-300 { animation-delay: 300ms; }
```

### Hover Effects

| Component | Tailwind Classes |
|-----------|-----------------|
| Primary Button | `hover:scale-[1.02] hover:shadow-lg hover:brightness-105 transition-all duration-200` |
| Feature Card | `hover:scale-[1.03] hover:-translate-y-1 hover:shadow-xl transition-all duration-200` |
| Secondary Button | `hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200` |

### Gradient Mesh Background

```tsx
// HeroSection.tsx - gradient mesh pattern
<div className="relative overflow-hidden">
  <div className="absolute inset-0 bg-gradient-to-br from-primary-500/20 via-accent-500/10 to-transparent" />
  <div className="absolute top-0 right-0 w-96 h-96 bg-accent-500/20 rounded-full blur-3xl" />
  <div className="absolute bottom-0 left-0 w-80 h-80 bg-primary-500/20 rounded-full blur-3xl" />
  {/* Content */}
</div>
```

### Animation Timing

| Animation | Duration | Easing |
|-----------|----------|--------|
| Entrance | 600ms | ease-out |
| Hover | 200ms | ease-out |
| Theme switch | 300ms | ease-in-out |
| Mobile menu | 250ms | ease-in-out |

---

## New Components to Create

### AnimatedSection.tsx
Wrapper component for entrance animations with stagger support.

### HeroSection.tsx
Homepage hero with gradient mesh background.

### CTASection.tsx
Call-to-action section with gradient background.

---

## Testing the Enhancements

### Animation Testing
1. Refresh homepage - sections should fade in with stagger
2. Hover over feature cards - should scale and lift
3. Hover over buttons - should scale with shadow
4. Toggle theme - transition should be smooth (300ms)

### Visual Testing
1. Check gradient renders correctly in both themes
2. Verify all text meets WCAG AA contrast
3. Confirm no layout shift during animations
4. Test at all breakpoints (320px, 768px, 1024px, 1440px)

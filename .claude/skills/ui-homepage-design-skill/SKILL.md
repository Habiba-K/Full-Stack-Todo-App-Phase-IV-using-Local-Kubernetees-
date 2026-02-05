---
name: ui-homepage-design-skill
description: Design modern, attractive, and responsive UI with a dedicated homepage and improved user experience for Next.js applications.
---

# UI & Homepage Design Skill

## Purpose
This skill focuses on improving the visual quality, usability, and responsiveness of a Next.js application. It ensures the application has a professional, attractive homepage and a smooth user journey from landing page to authentication and dashboard.

## Included Skills
- **UI Design Skill** – Modern layouts, visual hierarchy, spacing, typography, and color systems
- **UX Optimization Skill** – Clear user flows, intuitive navigation, and reduced friction
- **Responsive Layout Skill** – Mobile-first, tablet-friendly, and desktop-optimized layouts
- **Homepage Design Skill** – Engaging landing pages that communicate product value

## Instructions

### 1. Homepage Structure
- Create a dedicated homepage at `/`
- Do not redirect users directly to login or dashboard
- Homepage must include:
  - Hero section with headline and call-to-action
  - Short product value description
  - Feature highlights (3–4 key points)
  - Primary actions: **Sign Up** and **Login**

### 2. UI Layout Guidelines
- Use modern layout systems:
  - CSS Grid and Flexbox
- Maintain consistent spacing and alignment
- Use a clean color palette with sufficient contrast
- Apply consistent typography across all pages

### 3. User Experience Optimization
- Clear navigation paths:
  - Homepage → Login / Signup → Dashboard
- Avoid clutter and unnecessary elements
- Provide visual feedback for interactions (hover, focus, loading)
- Ensure forms are easy to scan and complete

### 4. Responsive Design Rules
- Mobile-first approach
- Components must adapt to:
  - Small screens (phones)
  - Medium screens (tablets)
  - Large screens (desktop)
- Avoid horizontal scrolling on any device
- Touch-friendly buttons and inputs

### 5. Component Styling
- Reusable UI components:
  - Buttons
  - Cards
  - Forms
  - Navigation bars
- Consistent border radius, shadows, and transitions
- Prefer subtle animations over heavy effects

### 6. Homepage Visual Enhancements
- Hero section should:
  - Capture attention immediately
  - Clearly explain what the app does
  - Contain a single primary CTA
- Optional enhancements:
  - Soft gradients or background patterns
  - Subtle entrance animations (fade, slide)
  - Icons for feature highlights

## Best Practices
- Keep headlines short and clear (under 12 words)
- One primary CTA per section
- Accessibility-first (contrast, readable font sizes)
- Performance-aware (no heavy animations blocking load)
- SEO-friendly homepage structure

## Example Homepage Structure
```html
<main>
  <section class="hero">
    <h1>Organize Your Tasks Effortlessly</h1>
    <p>A simple, secure, and fast todo app for everyday productivity.</p>
    <div class="cta-group">
      <a href="/signup" class="btn-primary">Get Started</a>
      <a href="/login" class="btn-secondary">Login</a>
    </div>
  </section>

  <section class="features">
    <div class="feature-card">Fast & Secure</div>
    <div class="feature-card">Multi-user Support</div>
    <div class="feature-card">Responsive Design</div>
  </section>
</main>

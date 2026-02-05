# Quickstart Guide: Frontend UI + API Integration

**Feature**: 002-frontend-todo-ui
**Date**: 2026-01-23
**Audience**: Developers setting up the Next.js frontend application

## Overview

This guide walks you through setting up the Next.js 16+ frontend application with Better Auth authentication and integration with the FastAPI backend. By the end, you'll have a fully functional todo application running locally.

## Prerequisites

**Required Software**:
- Node.js 18+ and npm/yarn/pnpm
- Git for version control
- Code editor (VS Code recommended)
- Backend API from SPEC 2 running (see backend README)

**Backend Requirements**:
- FastAPI backend must be running on http://localhost:8000
- Backend must have CORS configured to allow http://localhost:3000
- Backend must accept JWT tokens in Authorization header
- Database must be accessible and migrations run

**Knowledge Requirements**:
- Basic React and TypeScript knowledge
- Understanding of Next.js App Router
- Familiarity with REST APIs

## Setup Steps

### Step 1: Create Next.js Project

Initialize a new Next.js 16+ project with TypeScript and Tailwind CSS:

```bash
# Create Next.js project
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir

cd frontend
```

**Configuration Options**:
- ✅ TypeScript: Yes
- ✅ ESLint: Yes
- ✅ Tailwind CSS: Yes
- ✅ App Router: Yes
- ✅ Import alias (@/*): Yes
- ❌ src/ directory: No (use root-level app/)

---

### Step 2: Install Dependencies

Install required packages for authentication, forms, and API integration:

```bash
# Core dependencies
npm install better-auth react-hook-form

# Development dependencies
npm install -D @types/node @types/react @types/react-dom
```

**Dependencies Explained**:
- `better-auth`: Authentication and session management
- `react-hook-form`: Form handling and validation
- TypeScript types for Node and React

---

### Step 3: Configure Environment Variables

Create `.env.local` file in the frontend root:

```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-secret-here-must-match-backend
NEXTAUTH_URL=http://localhost:3000

# Database (same as backend)
DATABASE_URL=postgresql://user:password@host/database
```

Create `.env.local.example` (commit this to git):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-here-minimum-32-characters
NEXTAUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://user:password@host/database
```

**Important**:
- `BETTER_AUTH_SECRET` must match the backend secret exactly
- `NEXT_PUBLIC_API_URL` must point to running backend
- Use `NEXT_PUBLIC_` prefix for client-side accessible variables

---

### Step 4: Create Project Structure

Set up the directory structure:

```bash
# Create directories
mkdir -p app/signup app/signin app/dashboard app/tasks/[id] app/tasks/[id]/edit
mkdir -p components/auth components/tasks components/ui
mkdir -p lib types

# Create placeholder files
touch lib/auth.ts lib/api-client.ts lib/utils.ts
touch types/task.ts types/user.ts types/index.ts
```

**Directory Structure**:
```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   ├── signup/
│   │   └── page.tsx
│   ├── signin/
│   │   └── page.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   └── tasks/
│       └── [id]/
│           ├── page.tsx
│           └── edit/
│               └── page.tsx
├── components/
│   ├── auth/
│   ├── tasks/
│   └── ui/
├── lib/
│   ├── auth.ts
│   ├── api-client.ts
│   └── utils.ts
├── types/
│   ├── task.ts
│   ├── user.ts
│   └── index.ts
└── styles/
    └── globals.css
```

---

### Step 5: Configure Better Auth

Create `lib/auth.ts`:

```typescript
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.NEXTAUTH_URL!,
  database: {
    url: process.env.DATABASE_URL!
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7 // 7 days
    }
  },
  jwt: {
    enabled: true,
    maxAge: 60 * 60 * 24 * 7 // 7 days
  }
})

// Export session helpers
export const getSession = auth.api.getSession
export const useSession = auth.useSession
```

---

### Step 6: Create API Client

Create `lib/api-client.ts`:

```typescript
import { getSession } from './auth'
import { redirect } from 'next/navigation'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const session = await getSession()
  const token = session?.session?.token

  if (!token) {
    redirect('/signin')
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options?.headers
    }
  })

  if (response.status === 401) {
    redirect('/signin')
  }

  if (response.status === 403) {
    throw new Error('Access forbidden')
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'API request failed')
  }

  return response.json()
}

export const api = {
  get: <T>(endpoint: string) => apiClient<T>(endpoint),
  post: <T>(endpoint: string, data: any) =>
    apiClient<T>(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  put: <T>(endpoint: string, data: any) =>
    apiClient<T>(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
  delete: <T>(endpoint: string) =>
    apiClient<T>(endpoint, { method: 'DELETE' }),
  patch: <T>(endpoint: string, data?: any) =>
    apiClient<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined
    })
}
```

---

### Step 7: Configure Tailwind CSS

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}
```

Update `app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors;
  }

  .btn-secondary {
    @apply bg-gray-200 text-gray-900 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors;
  }

  .input-field {
    @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500;
  }
}
```

---

### Step 8: Start Development Server

Start the Next.js development server:

```bash
npm run dev
```

The application will be available at http://localhost:3000

**Verify Setup**:
1. Visit http://localhost:3000
2. You should see the landing page
3. Navigate to /signup to test the signup page
4. Check browser console for any errors

---

## Testing the Application

### 1. Test Backend Connection

Verify the backend is accessible:

```bash
curl http://localhost:8000/
# Should return: {"message": "Todo API with Authentication"}
```

### 2. Test Signup Flow

1. Navigate to http://localhost:3000/signup
2. Enter email, password, and name
3. Submit the form
4. Verify account created in backend database
5. Check redirect to dashboard

### 3. Test Signin Flow

1. Navigate to http://localhost:3000/signin
2. Enter credentials from signup
3. Submit the form
4. Verify JWT token received
5. Check redirect to dashboard

### 4. Test Task Operations

**Create Task**:
```bash
# After signing in, use browser DevTools Network tab
# POST http://localhost:8000/api/{user_id}/tasks
# Should include Authorization: Bearer <token>
```

**List Tasks**:
```bash
# GET http://localhost:8000/api/{user_id}/tasks
# Should return array of tasks
```

**Toggle Completion**:
```bash
# PATCH http://localhost:8000/api/{user_id}/tasks/{task_id}/complete
# Should update task completion status
```

---

## Common Issues and Solutions

### Issue 1: "CORS policy" error in browser console

**Symptoms**: API requests fail with CORS error

**Causes**:
- Backend CORS not configured for http://localhost:3000
- Backend not running

**Solutions**:
1. Verify backend CORS_ORIGINS includes http://localhost:3000
2. Restart backend server after CORS configuration change
3. Check backend logs for CORS-related errors

### Issue 2: "401 Unauthorized" on all API requests

**Symptoms**: All API calls return 401, even after signin

**Causes**:
- JWT token not included in requests
- BETTER_AUTH_SECRET mismatch between frontend and backend
- Token expired

**Solutions**:
1. Verify BETTER_AUTH_SECRET matches in both .env files
2. Check browser DevTools Network tab for Authorization header
3. Clear cookies and sign in again
4. Verify token format: `Bearer <token>`

### Issue 3: "Module not found" errors

**Symptoms**: Import errors for components or utilities

**Causes**:
- Incorrect import paths
- Missing files
- TypeScript configuration issues

**Solutions**:
1. Verify file exists at import path
2. Check tsconfig.json paths configuration
3. Restart TypeScript server in VS Code
4. Run `npm install` to ensure dependencies installed

### Issue 4: Tailwind styles not applying

**Symptoms**: Components have no styling

**Causes**:
- Tailwind not configured correctly
- Content paths incorrect in tailwind.config.js
- globals.css not imported

**Solutions**:
1. Verify tailwind.config.js content paths include all component files
2. Check app/layout.tsx imports globals.css
3. Restart development server
4. Clear Next.js cache: `rm -rf .next`

### Issue 5: Better Auth session not persisting

**Symptoms**: User logged out on page refresh

**Causes**:
- Cookie settings incorrect
- Database connection issues
- Session configuration wrong

**Solutions**:
1. Verify DATABASE_URL is correct
2. Check Better Auth configuration in lib/auth.ts
3. Verify cookies are enabled in browser
4. Check browser DevTools Application tab for cookies

---

## Development Workflow

### Running the Application

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Run type checking
npx tsc --noEmit
```

### Making Changes

1. **Add New Component**:
   - Create file in appropriate directory (components/tasks/, components/ui/, etc.)
   - Export component
   - Import and use in pages

2. **Add New Page**:
   - Create directory in app/ with page.tsx
   - Implement page component
   - Add navigation link

3. **Add New API Endpoint**:
   - Add endpoint to lib/api-client.ts
   - Create TypeScript types in types/
   - Use in components

### Code Quality

```bash
# Format code
npx prettier --write .

# Check types
npx tsc --noEmit

# Lint code
npm run lint
```

---

## Production Deployment

### Environment Variables

Set these in your production environment:

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
BETTER_AUTH_SECRET=<production-secret-32+-chars>
NEXTAUTH_URL=https://yourdomain.com
DATABASE_URL=<production-database-url>
```

### Build and Deploy

```bash
# Build for production
npm run build

# Test production build locally
npm start

# Deploy to Vercel (recommended for Next.js)
vercel deploy

# Or deploy to other platforms
# Follow platform-specific instructions
```

### Production Checklist

- [ ] Environment variables configured
- [ ] HTTPS enabled
- [ ] CORS configured for production domain
- [ ] Database connection secure
- [ ] Error logging enabled
- [ ] Performance monitoring set up
- [ ] Responsive design tested on real devices
- [ ] Authentication flow tested end-to-end
- [ ] All API endpoints tested
- [ ] Browser compatibility verified

---

## Additional Resources

**Next.js Documentation**: https://nextjs.org/docs
**Better Auth Documentation**: https://better-auth.com/docs
**Tailwind CSS Documentation**: https://tailwindcss.com/docs
**React Hook Form Documentation**: https://react-hook-form.com/

**Backend API Documentation**: See backend README and OpenAPI docs at http://localhost:8000/docs

---

## Support

If you encounter issues not covered in this guide:

1. Check the [research.md](./research.md) for technical decisions
2. Review [data-model.md](./data-model.md) for type definitions
3. Consult [plan.md](./plan.md) for architectural details
4. Check backend logs for API errors
5. Use browser DevTools Network tab to debug API calls

For bugs or feature requests, create an issue in the project repository.

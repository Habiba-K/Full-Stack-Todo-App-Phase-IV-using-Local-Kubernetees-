# Frontend - Todo Application

A modern, responsive Next.js 16+ frontend application with Better Auth authentication and FastAPI backend integration.

## Overview

This is the frontend component of a full-stack todo management application. It provides a complete user interface for task management with secure authentication, responsive design, and real-time API integration.

**Key Features**:
- User registration and authentication (Better Auth)
- Task CRUD operations (Create, Read, Update, Delete)
- Task completion toggling
- Responsive design (mobile, tablet, desktop)
- Loading states and error handling
- JWT-based API authentication

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS 4.0
- **Authentication**: Better Auth
- **Forms**: React Hook Form
- **API Client**: Custom fetch wrapper with JWT injection

## Prerequisites

Before setting up the frontend, ensure you have:

- **Node.js**: Version 18 or higher
- **Package Manager**: npm, yarn, or pnpm
- **Backend API**: FastAPI backend running on http://localhost:8000
- **Database**: PostgreSQL database accessible (shared with backend)

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Create a `.env.local` file in the frontend directory:

```env
# Backend API URL (must be accessible from browser)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-must-match-backend
NEXTAUTH_URL=http://localhost:3000

# Database Connection (same as backend)
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
```

**Important Notes**:
- `BETTER_AUTH_SECRET` must match the backend secret exactly
- `NEXT_PUBLIC_API_URL` must point to the running FastAPI backend
- `DATABASE_URL` should match the backend database configuration
- Never commit `.env.local` to version control

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

### 4. Build for Production

```bash
npm run build
npm start
```

## Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | Yes | `http://localhost:8000` |
| `BETTER_AUTH_SECRET` | Secret key for JWT signing (min 32 chars) | Yes | `your-secret-key-here` |
| `NEXTAUTH_URL` | Frontend application URL | Yes | `http://localhost:3000` |
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql://user:pass@host/db` |

**Security Notes**:
- Use strong, randomly generated secrets in production
- Use HTTPS URLs in production environments
- Store secrets in secure environment variable management systems

## Project Structure

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── dashboard/           # Main dashboard page
│   ├── signin/              # Sign in page
│   ├── signup/              # Sign up page
│   ├── tasks/               # Task-related pages
│   │   └── [id]/           # Dynamic task routes
│   │       ├── page.tsx    # Task detail page
│   │       └── edit/       # Task edit page
│   ├── layout.tsx          # Root layout with providers
│   └── page.tsx            # Landing page
├── components/              # React components
│   ├── auth/               # Authentication components
│   │   ├── SigninForm.tsx
│   │   └── SignupForm.tsx
│   ├── tasks/              # Task management components
│   │   ├── TaskCard.tsx
│   │   ├── TaskForm.tsx
│   │   └── TaskList.tsx
│   └── ui/                 # Reusable UI components
│       ├── Button.tsx
│       ├── Card.tsx
│       ├── ConfirmDialog.tsx
│       ├── ErrorMessage.tsx
│       ├── Input.tsx
│       └── Loading.tsx
├── lib/                     # Utility libraries
│   ├── api-client.ts       # API client with JWT injection
│   ├── auth.ts             # Better Auth configuration
│   └── utils.ts            # Helper functions
├── types/                   # TypeScript type definitions
│   ├── user.ts             # User-related types
│   ├── task.ts             # Task-related types
│   └── index.ts            # Type exports
├── .env.local              # Environment variables (not committed)
├── .env.local.example      # Environment template (committed)
├── .gitignore              # Git ignore rules
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind CSS configuration
└── tsconfig.json           # TypeScript configuration
```

## Authentication Flow

### Sign Up Flow
1. User fills out signup form (email, password, optional name)
2. Form validates input (email format, password min 8 chars)
3. POST request to `/api/auth/signup`
4. Backend creates user and returns JWT token
5. Better Auth stores token in secure session
6. User redirected to dashboard

### Sign In Flow
1. User enters credentials (email, password)
2. Form validates input
3. POST request to `/api/auth/signin`
4. Backend validates credentials and returns JWT token
5. Better Auth stores token in secure session
6. User redirected to dashboard

### Session Management
- JWT tokens stored in httpOnly cookies (secure)
- Token expiration: 7 days
- Automatic token refresh on API calls
- 401 responses trigger redirect to signin page

### Sign Out Flow
1. User clicks "Sign Out" button
2. Better Auth clears session and token
3. User redirected to signin page

## API Integration

### API Client Configuration

The application uses a custom API client (`lib/api-client.ts`) that:
- Automatically injects JWT tokens from Better Auth session
- Handles authentication errors (401 → redirect to signin)
- Handles authorization errors (403 → show error)
- Provides typed request/response handling

### API Endpoints Used

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/auth/signup` | POST | Create new user account | No |
| `/api/auth/signin` | POST | Authenticate user | No |
| `/api/auth/logout` | POST | Sign out user | Yes |
| `/api/{user_id}/tasks` | GET | List user's tasks | Yes |
| `/api/{user_id}/tasks` | POST | Create new task | Yes |
| `/api/{user_id}/tasks/{id}` | GET | Get task details | Yes |
| `/api/{user_id}/tasks/{id}` | PUT | Update task | Yes |
| `/api/{user_id}/tasks/{id}` | DELETE | Delete task | Yes |
| `/api/{user_id}/tasks/{id}/complete` | PATCH | Toggle task completion | Yes |

### Request Headers

All authenticated requests include:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Error Handling

The API client handles errors as follows:
- **401 Unauthorized**: Redirect to signin page
- **403 Forbidden**: Show "Access forbidden" error
- **404 Not Found**: Show "Resource not found" error
- **5xx Server Error**: Show "Server error, try again" message
- **Network Error**: Show "Connection failed" message

## Features

### User Authentication
- ✅ User registration with email and password
- ✅ User signin with credentials
- ✅ Secure JWT token management
- ✅ Session persistence (7 days)
- ✅ Logout functionality
- ✅ Protected routes (redirect if not authenticated)

### Task Management
- ✅ View all tasks in a list
- ✅ Create new tasks (title + optional description)
- ✅ View task details
- ✅ Edit existing tasks
- ✅ Delete tasks (with confirmation)
- ✅ Toggle task completion status
- ✅ Real-time UI updates

### User Experience
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Loading states for async operations
- ✅ Error messages with retry options
- ✅ Empty states when no tasks exist
- ✅ Success feedback for actions
- ✅ Confirmation dialogs for destructive actions
- ✅ Smooth transitions and animations

## Responsive Design

The application is fully responsive with breakpoints:
- **Mobile**: 320px - 639px (single column, touch-friendly)
- **Tablet**: 640px - 1023px (comfortable spacing)
- **Desktop**: 1024px+ (multi-column layout)

**Mobile Optimizations**:
- Touch-friendly button sizes (min 44px)
- Full-width forms and cards
- Simplified navigation
- Optimized font sizes

## Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

### Code Style

- **TypeScript**: Strict mode enabled
- **Components**: Functional components with hooks
- **Styling**: Tailwind CSS utility classes
- **Forms**: React Hook Form with validation
- **State**: React useState and useEffect hooks

### Adding New Features

1. Create TypeScript types in `types/`
2. Build reusable UI components in `components/ui/`
3. Create feature components in `components/[feature]/`
4. Add pages in `app/[route]/page.tsx`
5. Update API client if new endpoints needed

## Testing

### Manual Testing Checklist

**Authentication**:
- [ ] Sign up with new account
- [ ] Sign in with existing account
- [ ] Sign out and verify redirect
- [ ] Try accessing protected routes without auth

**Task Operations**:
- [ ] Create a new task
- [ ] View task list
- [ ] Click task to view details
- [ ] Edit task and save changes
- [ ] Toggle task completion
- [ ] Delete task with confirmation

**Responsive Design**:
- [ ] Test on mobile viewport (320px)
- [ ] Test on tablet viewport (768px)
- [ ] Test on desktop viewport (1024px+)
- [ ] Verify touch targets on mobile

**Error Handling**:
- [ ] Test with backend offline
- [ ] Test with invalid credentials
- [ ] Test with expired token
- [ ] Verify error messages display correctly

## Deployment

### Production Checklist

- [ ] Set `NEXT_PUBLIC_API_URL` to production backend URL
- [ ] Use HTTPS for all URLs
- [ ] Generate strong `BETTER_AUTH_SECRET` (32+ characters)
- [ ] Configure CORS on backend to allow frontend domain
- [ ] Enable production optimizations in Next.js
- [ ] Set up environment variables in hosting platform
- [ ] Test authentication flow in production
- [ ] Verify API requests include JWT tokens
- [ ] Test responsive design on real devices

### Recommended Hosting

- **Vercel**: Native Next.js support, automatic deployments
- **Netlify**: Good Next.js support, easy setup
- **AWS Amplify**: Full-stack hosting with backend integration
- **Docker**: Containerized deployment for any platform

## Troubleshooting

### Common Issues

**"Failed to load tasks" error**:
- Verify backend is running on correct URL
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS is configured on backend
- Check browser console for network errors

**Authentication not working**:
- Verify `BETTER_AUTH_SECRET` matches backend
- Check `DATABASE_URL` is correct
- Ensure database migrations are run
- Clear browser cookies and try again

**Styles not loading**:
- Run `npm install` to ensure Tailwind is installed
- Check `tailwind.config.js` configuration
- Restart development server

**TypeScript errors**:
- Run `npm install` to ensure types are installed
- Check `tsconfig.json` configuration
- Restart TypeScript server in IDE

## Contributing

When contributing to this project:
1. Follow existing code style and patterns
2. Add TypeScript types for all new code
3. Test on multiple screen sizes
4. Handle loading and error states
5. Update this README if adding new features

## Support

For issues or questions:
- Check the troubleshooting section above
- Review backend README for API documentation
- Check browser console for error messages
- Verify environment variables are set correctly

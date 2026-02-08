# Phase IV - Local Kubernetes Deployment (Minikube)

A full-stack Todo application with AI chatbot, deployed locally on Kubernetes using Minikube and Helm.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Local Machine (WSL2)                    │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │               Minikube Cluster                      │  │
│  │                                                     │  │
│  │  ┌──────────────────┐   ┌───────────────────────┐  │  │
│  │  │  Frontend Pod     │   │   Backend Pod          │  │  │
│  │  │  (Next.js)        │   │   (FastAPI + Groq AI)  │  │  │
│  │  │  Port: 3000       │   │   Port: 8000           │  │  │
│  │  │  NodePort: 30080  │   │   NodePort: 30081      │  │  │
│  │  └──────────────────┘   └──────────┬────────────┘  │  │
│  │                                     │               │  │
│  └─────────────────────────────────────┼───────────────┘  │
│                                        │                   │
│    kubectl port-forward               │                   │
│    (localhost:3000, localhost:39443)    │                   │
└────────────────────────────────────────┼───────────────────┘
                                         │
                          ┌──────────────┴──────────────┐
                          │                             │
                          ▼                             ▼
                ┌──────────────────┐        ┌────────────────┐
                │ Neon PostgreSQL  │        │   Groq API     │
                │ (Cloud DB)       │        │ (LLaMA 3.3 70B)│
                └──────────────────┘        └────────────────┘
```

## Tech Stack

| Layer         | Technology                    |
|---------------|-------------------------------|
| Frontend      | Next.js 15 (React, App Router)|
| Backend       | FastAPI (Python 3.11)         |
| Database      | Neon Serverless PostgreSQL    |
| Auth          | JWT (PyJWT + bcrypt)          |
| AI Agent      | Groq SDK + LLaMA 3.3 70B     |
| MCP Server    | Custom MCP tool server        |
| Container     | Docker                        |
| Orchestration | Kubernetes (Minikube)         |
| Packaging     | Helm Chart                    |

## Project Structure

```
Phase-IV-Local-Kubernetees/
├── frontend/                  # Next.js frontend application
│   ├── Dockerfile             # Multi-stage Docker build
│   ├── app/                   # App Router pages
│   │   ├── page.tsx           # Homepage
│   │   ├── signin/            # Sign in page
│   │   ├── signup/            # Sign up page
│   │   ├── dashboard/         # Todo dashboard
│   │   └── chat/              # AI chatbot interface
│   ├── components/            # React components
│   │   ├── auth/              # Auth forms (SigninForm, SignupForm)
│   │   ├── chat/              # Chat UI (ChatContainer)
│   │   └── ui/                # Shared UI components
│   ├── lib/                   # API client, auth helpers
│   └── package.json
│
├── backend/                   # FastAPI backend application
│   ├── Dockerfile             # Python Docker build
│   ├── src/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Settings (env vars)
│   │   ├── database.py        # Async SQLAlchemy + Neon
│   │   ├── models/            # SQLModel entities (User, Task, Conversation, Message)
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── routers/           # API endpoints (auth, tasks, chat)
│   │   ├── services/          # Business logic (task_service, chat_service, agent_service)
│   │   ├── auth/              # JWT auth (utils, dependencies, schemas)
│   │   └── mcp/               # MCP tool server (server, tools, schemas)
│   └── requirements.txt
│
├── todo-chatbot/              # Helm Chart
│   ├── Chart.yaml             # Chart metadata (v0.1.0)
│   ├── values.yaml            # Configuration values
│   └── templates/
│       ├── deployment.yaml    # Frontend + Backend Deployments
│       ├── service.yaml       # NodePort Services
│       ├── serviceaccount.yaml
│       ├── ingress.yaml       # Ingress (disabled for local)
│       └── hpa.yaml           # Horizontal Pod Autoscaler (disabled for local)
│
└── README.md
```

## Features

- **User Authentication** - Signup/Signin with JWT tokens and bcrypt password hashing
- **Todo CRUD** - Create, Read, Update, Delete todos via REST API or AI chatbot
- **Mark Complete/Incomplete** - Toggle todo status
- **AI Chatbot** - Natural language task management powered by Groq LLaMA 3.3 70B
- **MCP Tool Server** - Model Context Protocol server for AI agent tool calling
- **Multi-user** - Data isolation per user (all queries scoped by user_id)
- **Responsive UI** - Works on desktop and mobile
- **Kubernetes Native** - Deployed via Helm chart on Minikube

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- A [Neon PostgreSQL](https://neon.tech) database (free tier)
- A [Groq API key](https://console.groq.com) for the AI chatbot

## Environment Variables

### Backend (`backend/.env`)

| Variable              | Required | Description                                     |
|-----------------------|----------|-------------------------------------------------|
| `DATABASE_URL`        | Yes      | Neon PostgreSQL connection string                |
| `GROQ_API_KEY`        | Yes      | Groq API key for AI agent                        |
| `GROQ_MODEL`          | No       | LLM model name (default: `llama-3.3-70b-versatile`) |
| `BETTER_AUTH_SECRET`  | Yes      | Secret key for JWT signing                       |
| `CORS_ORIGINS`        | No       | Allowed CORS origins (default: `http://localhost:3000`) |
| `CHAT_CONTEXT_MESSAGES` | No     | Chat history window size (default: `50`)         |

### Frontend (`frontend/.env.local`)

| Variable              | Required | Description                              |
|-----------------------|----------|------------------------------------------|
| `NEXT_PUBLIC_API_URL` | Yes      | Backend API URL (used at build time)     |
| `BETTER_AUTH_SECRET`  | Yes      | Same secret as backend                   |
| `DATABASE_URL`        | Yes      | Same Neon connection string              |

## Deployment Steps

### 1. Start Minikube

```bash
minikube start
```

### 2. Configure Minikube Docker Environment

Point your shell to minikube's Docker daemon so images are built directly inside the cluster:

```bash
eval $(minikube docker-env)
```

### 3. Build Docker Images

```bash
# Build backend image
docker build -t todo-backend:latest ./backend

# Build frontend image (API URL is baked at build time)
docker build -t todo-frontend:latest ./frontend
```

### 4. Deploy with Helm

```bash
helm install todo-chatbot ./todo-chatbot
```

### 5. Verify Deployment

```bash
# Check pods are running
kubectl get pods

# Check services
kubectl get svc
```

### 6. Access the Application

Use `kubectl port-forward` for stable local access:

```bash
# Forward frontend (port 3000)
kubectl port-forward svc/todo-chatbot-frontend 3000:3000 &

# Forward backend (port must match NEXT_PUBLIC_API_URL baked into frontend)
kubectl port-forward svc/todo-chatbot-backend 39443:8000 &
```

Open in browser:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:39443
- **API Docs (Swagger):** http://localhost:39443/docs

### Updating After Code Changes

```bash
# Ensure minikube Docker env is active
eval $(minikube docker-env)

# Rebuild the changed image
docker build -t todo-backend:latest ./backend

# Restart the deployment to pick up the new image
kubectl rollout restart deployment todo-chatbot-backend

# Wait for rollout
kubectl rollout status deployment todo-chatbot-backend
```

## Kubernetes Resources

| Resource   | Name                    | Type       | Port            |
|------------|-------------------------|------------|-----------------|
| Deployment | todo-chatbot-frontend   | 1 replica  | Container: 3000 |
| Deployment | todo-chatbot-backend    | 1 replica  | Container: 8000 |
| Service    | todo-chatbot-frontend   | NodePort   | 30080 -> 3000   |
| Service    | todo-chatbot-backend    | NodePort   | 30081 -> 8000   |

## Helm Chart Configuration

Key values in `todo-chatbot/values.yaml`:

| Parameter                     | Description              | Default          |
|-------------------------------|--------------------------|------------------|
| `frontend.image.repository`   | Frontend Docker image    | `todo-frontend`  |
| `frontend.image.pullPolicy`   | Image pull policy        | `Never` (local)  |
| `frontend.service.nodePort`   | Frontend NodePort        | `30080`          |
| `backend.image.repository`    | Backend Docker image     | `todo-backend`   |
| `backend.image.pullPolicy`    | Image pull policy        | `Never` (local)  |
| `backend.service.nodePort`    | Backend NodePort         | `30081`          |
| `backend.env.GROQ_API_KEY`    | Groq API key             | (set in values)  |
| `backend.env.GROQ_MODEL`      | LLM model                | `llama-3.3-70b-versatile` |
| `replicaCount`                | Pod replicas             | `1`              |

## Useful Commands

```bash
# Check cluster status
minikube status

# View all Kubernetes resources
kubectl get all

# View running pods
kubectl get pods -o wide

# View services
kubectl get services

# Check Helm releases
helm list

# View pod logs (live)
kubectl logs -f deployment/todo-chatbot-backend
kubectl logs -f deployment/todo-chatbot-frontend

# Restart a deployment (after image rebuild)
kubectl rollout restart deployment todo-chatbot-backend

# Open Kubernetes Dashboard
minikube dashboard

# Uninstall
helm uninstall todo-chatbot

# Stop Minikube
minikube stop
```

## Docker Images

| Image            | Base             | Description                           |
|------------------|------------------|---------------------------------------|
| todo-frontend    | node:20-alpine   | Multi-stage build (Next.js standalone)|
| todo-backend     | python:3.11-slim | FastAPI + Groq SDK + MCP server       |

## API Endpoints

### Authentication
| Method | Endpoint             | Description         |
|--------|----------------------|---------------------|
| POST   | `/api/auth/signup`   | Create new account  |
| POST   | `/api/auth/signin`   | Login & get JWT     |
| POST   | `/api/auth/logout`   | Logout              |
| GET    | `/api/auth/me`       | Get current user    |

### Tasks (Protected - require JWT)
| Method | Endpoint                      | Description              |
|--------|-------------------------------|--------------------------|
| POST   | `/api/todos`                  | Create todo              |
| GET    | `/api/todos`                  | List user's todos        |
| GET    | `/api/todos/{id}`             | Get single todo          |
| PUT    | `/api/todos/{id}`             | Update todo              |
| DELETE | `/api/todos/{id}`             | Delete todo              |
| PATCH  | `/api/todos/{id}/complete`    | Mark as complete         |
| PATCH  | `/api/todos/{id}/incomplete`  | Mark as incomplete       |

### AI Chatbot (Protected)
| Method | Endpoint           | Description                        |
|--------|--------------------|------------------------------------|
| POST   | `/api/chat`        | Send message to AI task assistant  |
| GET    | `/api/chat/history`| Get conversation history           |

## AI Chatbot

The chatbot uses a Groq-powered AI agent with MCP (Model Context Protocol) tool calling to manage tasks through natural language.

**Available MCP Tools:**
| Tool            | Description                             |
|-----------------|-----------------------------------------|
| `add_task`      | Create a new task                       |
| `list_tasks`    | List tasks with optional status filter  |
| `get_task`      | Get a specific task by ID               |
| `update_task`   | Update task title or description        |
| `complete_task` | Mark a task as complete                 |
| `delete_task`   | Delete a task permanently               |

**Example chat interactions:**
- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark task 1 as complete"
- "Delete the second task"

## Troubleshooting

### Chat returns "I'm having trouble processing your request"
Check backend pod logs for the actual error:
```bash
kubectl logs deployment/todo-chatbot-backend --tail=50
```
Common causes: Groq SDK version incompatibility with httpx, invalid API key, or database connection issues.

### Pods stuck in CrashLoopBackOff
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous
```

### Port forwarding stops working after pod restart
Re-establish port forwarding:
```bash
kubectl port-forward svc/todo-chatbot-backend 39443:8000 &
```

### CORS errors in browser console
Ensure the backend's `CORS_ORIGINS` env var includes the frontend URL (e.g., `http://localhost:3000`).

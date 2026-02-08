# Phase IV - Local Kubernetes Deployment (Minikube)

A full-stack Todo application with AI chatbot, deployed locally on Kubernetes using Minikube and Helm.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                  Local Machine (WSL2)                │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │              Minikube Cluster                  │  │
│  │                                               │  │
│  │  ┌─────────────────┐  ┌────────────────────┐  │  │
│  │  │   Frontend Pod   │  │   Backend Pod      │  │  │
│  │  │   (Next.js)      │  │   (FastAPI)        │  │  │
│  │  │   Port: 3000     │  │   Port: 8000       │  │  │
│  │  │   NodePort:30080 │  │   NodePort: 30081  │  │  │
│  │  └─────────────────┘  └────────┬───────────┘  │  │
│  │                                │              │  │
│  └────────────────────────────────┼──────────────┘  │
│                                   │                 │
└───────────────────────────────────┼─────────────────┘
                                    │
                                    ▼
                        ┌───────────────────┐
                        │   Neon PostgreSQL  │
                        │   (Cloud DB)       │
                        └───────────────────┘
```

## Tech Stack

| Layer        | Technology                  |
|--------------|-----------------------------|
| Frontend     | Next.js 16 (React)          |
| Backend      | FastAPI (Python 3.11)       |
| Database     | Neon Serverless PostgreSQL   |
| Auth         | Better Auth (JWT)           |
| AI Chatbot   | Groq API (LLaMA 3.3 70B)   |
| Container    | Docker                      |
| Orchestration| Kubernetes (Minikube)       |
| Packaging    | Helm Chart                  |

## Project Structure

```
Phase-IV-Local-Kubernetees/
├── frontend/                  # Next.js frontend application
│   ├── Dockerfile             # Multi-stage Docker build
│   ├── src/
│   │   └── app/               # App Router pages
│   │       ├── signin/        # Sign in page
│   │       ├── signup/        # Sign up page
│   │       ├── dashboard/     # Todo dashboard
│   │       └── chat/          # AI chatbot
│   └── package.json
│
├── backend/                   # FastAPI backend application
│   ├── Dockerfile             # Python Docker build
│   ├── src/
│   │   └── main.py            # API entry point
│   └── requirements.txt
│
├── todo-chatbot/              # Helm Chart
│   ├── Chart.yaml             # Chart metadata
│   ├── values.yaml            # Configuration values
│   └── templates/
│       ├── deployment.yaml    # Frontend + Backend Deployments
│       ├── service.yaml       # NodePort Services
│       ├── serviceaccount.yaml
│       ├── ingress.yaml
│       ├── hpa.yaml           # Horizontal Pod Autoscaler
│       └── NOTES.txt          # Post-install notes
│
└── README.md
```

## Features

- **User Authentication** - Signup/Signin with JWT tokens (Better Auth)
- **Todo CRUD** - Create, Read, Update, Delete todos
- **Mark Complete/Incomplete** - Toggle todo status
- **AI Chatbot** - Chat with AI assistant about your todos (Groq LLaMA 3.3)
- **Multi-user** - Data isolation per user
- **Responsive UI** - Works on desktop and mobile

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)

## Deployment Steps

### 1. Start Minikube

```bash
minikube start
```

### 2. Build Docker Images

```bash
# Build frontend image
docker build --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 \
  -t todo-frontend:latest ./frontend

# Build backend image
docker build -t todo-backend:latest ./backend
```

### 3. Load Images into Minikube

```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 4. Deploy with Helm

```bash
helm install todo-chatbot ./todo-chatbot
```

### 5. Access the Application

```bash
# Port-forward for stable access
kubectl port-forward service/todo-chatbot-frontend 3000:3000 &
kubectl port-forward service/todo-chatbot-backend 8000:8000 &
```

Open in browser:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs

## Kubernetes Resources

| Resource   | Name                    | Type       | Port          |
|------------|-------------------------|------------|---------------|
| Deployment | todo-chatbot-frontend   | 1 replica  | Container 3000|
| Deployment | todo-chatbot-backend    | 1 replica  | Container 8000|
| Service    | todo-chatbot-frontend   | NodePort   | 30080 → 3000  |
| Service    | todo-chatbot-backend    | NodePort   | 30081 → 8000  |

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

# View pod logs
kubectl logs deployment/todo-chatbot-frontend
kubectl logs deployment/todo-chatbot-backend

# Open Kubernetes Dashboard
minikube dashboard

# Uninstall
helm uninstall todo-chatbot

# Stop Minikube
minikube stop
```

## Docker Images

| Image            | Base             | Size   | Description                    |
|------------------|------------------|--------|--------------------------------|
| todo-frontend    | node:20-alpine   | ~293MB | Multi-stage build (standalone) |
| todo-backend     | python:3.11-slim | ~594MB | FastAPI with uvicorn           |

## API Endpoints

### Authentication
| Method | Endpoint             | Description         |
|--------|----------------------|---------------------|
| POST   | `/api/auth/signup`   | Create new account  |
| POST   | `/api/auth/signin`   | Login & get JWT     |
| POST   | `/api/auth/logout`   | Logout              |
| GET    | `/api/auth/me`       | Get current user    |

### Todos (Protected - require JWT)
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
| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| POST   | `/api/chat`        | Chat with AI assistant   |
| GET    | `/api/chat/history`| Get chat history         |

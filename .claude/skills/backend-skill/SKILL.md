---
name: backend-skill
description: Generate backend routes, handle requests and responses, and connect to databases. Use for API and server-side development.
---

# Backend Skill – Routes, Requests/Responses, Database Integration

## Instructions

1. **Route Generation**
   - Design RESTful endpoints with clear URL structures
   - Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
   - Group routes by resource or domain
   - Apply versioning when needed (e.g., `/api/v1`)

2. **Request & Response Handling**
   - Validate incoming requests using schemas (e.g., Pydantic)
   - Enforce consistent response formats
   - Use correct HTTP status codes
   - Implement proper error handling and logging

3. **Authentication & Authorization**
   - Integrate auth mechanisms (JWT, OAuth2, API keys)
   - Protect routes with role- or permission-based access
   - Handle token validation and expiration securely

4. **Database Connection**
   - Connect to databases using ORM or query builders
   - Implement CRUD operations efficiently
   - Manage transactions and connection lifecycles
   - Prevent SQL injection and unsafe queries

## Best Practices
- Keep controllers thin; move logic to services
- Validate all external inputs
- Use async I/O where supported
- Handle failures gracefully
- Document APIs with OpenAPI/Swagger
- Write reusable and testable code

## Example Structure
```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

class UserCreate(BaseModel):
    email: str
    password: str

@app.post("/users", status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = create_user_service(db, payload)
    return {"id": user.id, "email": user.email}

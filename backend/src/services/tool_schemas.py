from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# Tool Input Schemas
class CreateTodoInput(BaseModel):
    """Input schema for create_todo tool."""
    title: str = Field(..., description="Task title (1-500 characters)", min_length=1, max_length=500)
    description: Optional[str] = Field(None, description="Task description (max 5000 characters)", max_length=5000)


class ListTodosInput(BaseModel):
    """Input schema for list_todos tool."""
    status: Optional[str] = Field("all", description="Filter by status: 'pending', 'completed', or 'all'")
    limit: Optional[int] = Field(20, description="Maximum number of tasks to return", ge=1, le=100)


class GetTodoInput(BaseModel):
    """Input schema for get_todo tool."""
    task_id: str = Field(..., description="UUID of the task to retrieve")


class UpdateTodoInput(BaseModel):
    """Input schema for update_todo tool."""
    task_id: str = Field(..., description="UUID of the task to update")
    title: Optional[str] = Field(None, description="New task title", max_length=500)
    description: Optional[str] = Field(None, description="New task description", max_length=5000)
    completed: Optional[bool] = Field(None, description="New completion status")


class DeleteTodoInput(BaseModel):
    """Input schema for delete_todo tool."""
    task_id: str = Field(..., description="UUID of the task to delete")


class CompleteTodoInput(BaseModel):
    """Input schema for complete_todo tool."""
    task_id: str = Field(..., description="UUID of the task to mark as complete")


class IncompleteTodoInput(BaseModel):
    """Input schema for incomplete_todo tool."""
    task_id: str = Field(..., description="UUID of the task to mark as incomplete")


# Tool Output Schemas
class TaskOutput(BaseModel):
    """Output schema for task objects."""
    id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str


class ListTodosOutput(BaseModel):
    """Output schema for list_todos tool."""
    tasks: List[TaskOutput]
    count: int


class DeleteTodoOutput(BaseModel):
    """Output schema for delete_todo tool."""
    success: bool
    message: str

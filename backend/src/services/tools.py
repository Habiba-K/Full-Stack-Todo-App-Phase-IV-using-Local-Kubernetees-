from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Dict, Any, List
from src.services import task_service
from src.services.tool_schemas import (
    CreateTodoInput, ListTodosInput, GetTodoInput, UpdateTodoInput,
    DeleteTodoInput, CompleteTodoInput, IncompleteTodoInput,
    TaskOutput, ListTodosOutput, DeleteTodoOutput
)
from src.schemas.task import TaskCreate, TaskUpdate


# Tool function definitions for Groq
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "create_todo",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title (1-500 characters)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (optional, max 5000 characters)"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_todos",
            "description": "List all tasks for the user with optional filtering",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by status (default: all)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tasks to return (default: 20)",
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_todo",
            "description": "Get a specific task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to retrieve"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_todo",
            "description": "Update a task's title, description, or completion status",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional)"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "New completion status (optional)"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_todo",
            "description": "Delete a task permanently",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_todo",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to mark as complete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "incomplete_todo",
            "description": "Mark a task as incomplete (not done)",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to mark as incomplete"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]


def task_to_dict(task) -> Dict[str, Any]:
    """Convert Task model to dictionary for tool output."""
    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


async def execute_tool(
    tool_name: str,
    tool_input: Dict[str, Any],
    db: AsyncSession,
    user_id: str
) -> Dict[str, Any]:
    """
    Execute a tool function and return the result.

    Args:
        tool_name: Name of the tool to execute
        tool_input: Tool input parameters
        db: Database session
        user_id: Authenticated user ID

    Returns:
        Tool execution result as dictionary
    """
    try:
        if tool_name == "create_todo":
            input_data = CreateTodoInput(**tool_input)
            task_data = TaskCreate(
                title=input_data.title,
                description=input_data.description
            )
            task = await task_service.create_task(db, user_id, task_data)
            return task_to_dict(task)

        elif tool_name == "list_todos":
            input_data = ListTodosInput(**tool_input)
            tasks = await task_service.get_user_tasks(db, user_id)

            # Apply status filter
            if input_data.status == "pending":
                tasks = [t for t in tasks if not t.completed]
            elif input_data.status == "completed":
                tasks = [t for t in tasks if t.completed]

            # Apply limit
            tasks = tasks[:input_data.limit]

            return {
                "tasks": [task_to_dict(t) for t in tasks],
                "count": len(tasks)
            }

        elif tool_name == "get_todo":
            input_data = GetTodoInput(**tool_input)
            task = await task_service.get_task_by_id(db, user_id, UUID(input_data.task_id))
            if not task:
                return {"error": "Task not found"}
            return task_to_dict(task)

        elif tool_name == "update_todo":
            input_data = UpdateTodoInput(**tool_input)
            task_data = TaskUpdate(
                title=input_data.title,
                description=input_data.description,
                completed=input_data.completed
            )
            task = await task_service.update_task(db, user_id, UUID(input_data.task_id), task_data)
            if not task:
                return {"error": "Task not found"}
            return task_to_dict(task)

        elif tool_name == "delete_todo":
            input_data = DeleteTodoInput(**tool_input)
            success = await task_service.delete_task(db, user_id, UUID(input_data.task_id))
            return {
                "success": success,
                "message": "Task deleted" if success else "Task not found"
            }

        elif tool_name == "complete_todo":
            input_data = CompleteTodoInput(**tool_input)
            task = await task_service.get_task_by_id(db, user_id, UUID(input_data.task_id))
            if not task:
                return {"error": "Task not found"}
            if not task.completed:
                task = await task_service.toggle_task_completion(db, user_id, UUID(input_data.task_id))
            return task_to_dict(task)

        elif tool_name == "incomplete_todo":
            input_data = IncompleteTodoInput(**tool_input)
            task = await task_service.get_task_by_id(db, user_id, UUID(input_data.task_id))
            if not task:
                return {"error": "Task not found"}
            if task.completed:
                task = await task_service.toggle_task_completion(db, user_id, UUID(input_data.task_id))
            return task_to_dict(task)

        else:
            return {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        return {"error": str(e)}

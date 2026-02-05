from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from src.database import get_session
from src.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from src.services import task_service
from src.auth.dependencies import get_current_user_id
from src.auth.utils import validate_ownership

router = APIRouter()


async def verify_ownership(
    user_id: UUID,
    current_user_id: Annotated[UUID, Depends(get_current_user_id)]
) -> UUID:
    """
    Verify that the authenticated user matches the path parameter user_id.

    Args:
        user_id: User ID from path parameter
        current_user_id: User ID from JWT token

    Returns:
        Authenticated user ID if validation passes

    Raises:
        HTTPException: 403 if user IDs don't match
    """
    if not validate_ownership(user_id, current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )
    return current_user_id


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_user_tasks(
    user_id: UUID,
    authenticated_user_id: Annotated[UUID, Depends(verify_ownership)],
    db: AsyncSession = Depends(get_session)
):
    """
    List all tasks for a specific user.

    Requires valid JWT token. User can only access their own tasks.

    Args:
        user_id: User identifier from path
        authenticated_user_id: Authenticated user ID from JWT
        db: Database session (injected)

    Returns:
        List of tasks belonging to the authenticated user

    Raises:
        HTTPException: 401 if not authenticated, 403 if accessing other user's data
    """
    try:
        tasks = await task_service.get_user_tasks(db, str(authenticated_user_id))
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    user_id: UUID,
    task_data: TaskCreate,
    authenticated_user_id: Annotated[UUID, Depends(verify_ownership)],
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new task for a specific user.

    Requires valid JWT token. User can only create tasks for themselves.

    Args:
        user_id: User identifier from path
        task_data: Task creation data (title, description)
        authenticated_user_id: Authenticated user ID from JWT
        db: Database session (injected)

    Returns:
        Created task with all fields

    Raises:
        HTTPException: 401 if not authenticated, 403 if creating for other user, 422 if validation fails
    """
    try:
        task = await task_service.create_task(db, str(authenticated_user_id), task_data)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: UUID,
    task_id: UUID,
    authenticated_user_id: Annotated[UUID, Depends(verify_ownership)],
    db: AsyncSession = Depends(get_session)
):
    """
    Get a specific task by ID for a specific user.

    Requires valid JWT token. User can only access their own tasks.

    Args:
        user_id: User identifier from path
        task_id: Task unique identifier
        authenticated_user_id: Authenticated user ID from JWT
        db: Database session (injected)

    Returns:
        Task details if found and belongs to authenticated user

    Raises:
        HTTPException: 401 if not authenticated, 403 if accessing other user's task, 404 if task not found
    """
    task = await task_service.get_task_by_id(db, str(authenticated_user_id), task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    authenticated_user_id: Annotated[UUID, Depends(verify_ownership)],
    db: AsyncSession = Depends(get_session)
):
    """
    Update an existing task for a specific user.

    Requires valid JWT token. User can only update their own tasks.

    Args:
        user_id: User identifier from path
        task_id: Task unique identifier
        task_data: Task update data (title, description, completed)
        authenticated_user_id: Authenticated user ID from JWT
        db: Database session (injected)

    Returns:
        Updated task with all fields

    Raises:
        HTTPException: 401 if not authenticated, 403 if updating other user's task, 404 if task not found, 422 if validation fails
    """
    try:
        task = await task_service.update_task(db, str(authenticated_user_id), task_id, task_data)
        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    authenticated_user_id: Annotated[UUID, Depends(verify_ownership)],
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a task for a specific user.

    Requires valid JWT token. User can only delete their own tasks.

    Args:
        user_id: User identifier from path
        task_id: Task unique identifier
        authenticated_user_id: Authenticated user ID from JWT
        db: Database session (injected)

    Returns:
        Success message

    Raises:
        HTTPException: 401 if not authenticated, 403 if deleting other user's task, 404 if task not found
    """
    success = await task_service.delete_task(db, str(authenticated_user_id), task_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: UUID,
    task_id: UUID,
    authenticated_user_id: Annotated[UUID, Depends(verify_ownership)],
    db: AsyncSession = Depends(get_session)
):
    """
    Toggle the completion status of a task.

    Requires valid JWT token. User can only toggle their own tasks.

    Args:
        user_id: User identifier from path
        task_id: Task unique identifier
        authenticated_user_id: Authenticated user ID from JWT
        db: Database session (injected)

    Returns:
        Updated task with toggled completion status

    Raises:
        HTTPException: 401 if not authenticated, 403 if toggling other user's task, 404 if task not found
    """
    task = await task_service.toggle_task_completion(db, str(authenticated_user_id), task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task


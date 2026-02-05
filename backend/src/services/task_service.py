from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate


async def get_user_tasks(db: AsyncSession, user_id: str) -> List[Task]:
    """
    Retrieve all tasks for a specific user.

    Args:
        db: Database session
        user_id: User identifier to filter tasks

    Returns:
        List of Task objects belonging to the user
    """
    result = await db.execute(
        select(Task).where(Task.user_id == user_id)
    )
    tasks = result.scalars().all()
    return list(tasks)


async def create_task(db: AsyncSession, user_id: str, task_data: TaskCreate) -> Task:
    """
    Create a new task for a specific user.

    Args:
        db: Database session
        user_id: User identifier to assign task to
        task_data: Task creation data (title, description)

    Returns:
        Created Task object with all fields populated
    """
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task_by_id(db: AsyncSession, user_id: str, task_id: UUID) -> Optional[Task]:
    """
    Retrieve a specific task by ID for a specific user.

    Args:
        db: Database session
        user_id: User identifier to enforce ownership
        task_id: Task unique identifier

    Returns:
        Task object if found and belongs to user, None otherwise
    """
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    return task


async def update_task(db: AsyncSession, user_id: str, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
    """
    Update an existing task for a specific user.

    Args:
        db: Database session
        user_id: User identifier to enforce ownership
        task_id: Task unique identifier
        task_data: Task update data (title, description, completed)

    Returns:
        Updated Task object if found and belongs to user, None otherwise
    """
    task = await get_task_by_id(db, user_id, task_id)
    if not task:
        return None

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, user_id: str, task_id: UUID) -> bool:
    """
    Delete a task for a specific user.

    Args:
        db: Database session
        user_id: User identifier to enforce ownership
        task_id: Task unique identifier

    Returns:
        True if task was deleted, False if not found or doesn't belong to user
    """
    task = await get_task_by_id(db, user_id, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True


async def toggle_task_completion(db: AsyncSession, user_id: str, task_id: UUID) -> Optional[Task]:
    """
    Toggle the completion status of a task.

    Args:
        db: Database session
        user_id: User identifier to enforce ownership
        task_id: Task unique identifier

    Returns:
        Updated Task object if found and belongs to user, None otherwise
    """
    task = await get_task_by_id(db, user_id, task_id)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)
    return task


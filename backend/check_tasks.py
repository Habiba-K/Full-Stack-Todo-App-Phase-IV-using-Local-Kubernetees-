import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from src.models.task import Task
from src.models.user import User

async def check_database():
    # Database connection
    DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_ypXWDUo0q4cd@ep-misty-paper-ahr6etdt-pooler.c-3.us-east-1.aws.neon.tech/neondb"

    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check users
        print("=== USERS ===")
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"  User ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.name}")
            print("---")

        # Check tasks
        print("\n=== TASKS ===")
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        print(f"Total tasks: {len(tasks)}")
        for task in tasks:
            print(f"  Task ID: {task.id}")
            print(f"  User ID: {task.user_id}")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description}")
            print(f"  Completed: {task.completed}")
            print(f"  Created: {task.created_at}")
            print("---")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_database())

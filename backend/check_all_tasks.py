import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from src.models.task import Task

async def check_tasks():
    DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_ypXWDUo0q4cd@ep-misty-paper-ahr6etdt-pooler.c-3.us-east-1.aws.neon.tech/neondb"

    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check new user tasks
        print("=" * 70)
        print("TASKS FOR NEW USER (ummehabiba1797@gmail.com)")
        print("User ID: f3ea363d-c1f7-4f88-bb80-31d59b16b068")
        print("=" * 70)

        result = await session.execute(
            select(Task).where(Task.user_id == 'f3ea363d-c1f7-4f88-bb80-31d59b16b068')
        )
        tasks = result.scalars().all()

        print(f"\nTotal tasks: {len(tasks)}\n")
        for i, task in enumerate(tasks, 1):
            status = "Completed" if task.completed else "Pending"
            print(f"{i}. {task.title}")
            print(f"   ID: {task.id}")
            print(f"   Status: {status}")
            print(f"   Created: {task.created_at}")
            print()

        # Check old user tasks
        print("=" * 70)
        print("TASKS FOR OLD USER (khabiba1797@gmail.com)")
        print("User ID: 3805678f-bfe2-4698-98c8-0c8a75f71b62")
        print("=" * 70)

        result = await session.execute(
            select(Task).where(Task.user_id == '3805678f-bfe2-4698-98c8-0c8a75f71b62')
        )
        tasks = result.scalars().all()

        print(f"\nTotal tasks: {len(tasks)}\n")
        for i, task in enumerate(tasks, 1):
            status = "Completed" if task.completed else "Pending"
            print(f"{i}. {task.title}")
            print(f"   ID: {task.id}")
            print(f"   Status: {status}")
            print(f"   Created: {task.created_at}")
            print()

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_tasks())

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database session injection.

    Usage:
        @app.get("/endpoint")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            # Use db session here
            pass

    Yields:
        AsyncSession: Database session for the request
    """
    async for session in get_session():
        yield session

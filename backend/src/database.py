from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings


# Convert postgresql:// to postgresql+asyncpg:// for async support
# Remove sslmode parameter as asyncpg handles SSL differently
database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
# Remove sslmode parameter if present (asyncpg doesn't use it)
if "sslmode=" in database_url:
    # Split by ? to separate base URL from parameters
    parts = database_url.split("?")
    if len(parts) > 1:
        base_url = parts[0]
        params = parts[1].split("&")
        # Filter out sslmode and channel_binding parameters
        filtered_params = [p for p in params if not p.startswith("sslmode=") and not p.startswith("channel_binding=")]
        if filtered_params:
            database_url = base_url + "?" + "&".join(filtered_params)
        else:
            database_url = base_url

# Create async engine for Neon PostgreSQL with connection pooling
engine = create_async_engine(
    database_url,
    echo=True,  # Set to False in production
    future=True,
    pool_pre_ping=True,  # Verify connections before using
)

# Create async session factory
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """
    Initialize database tables.
    Called on application startup.
    """
    async with engine.begin() as conn:
        # Create all tables defined in SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """
    Dependency for getting async database session.
    Yields a session and ensures it's closed after use.
    """
    async with async_session_maker() as session:
        yield session

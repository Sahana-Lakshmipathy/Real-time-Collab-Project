from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from app.core.config import get_settings

settings = get_settings()

# ----------------------------------------
# Base class for declarative models
# ----------------------------------------
class Base(DeclarativeBase):
    pass

# ----------------------------------------
# Create async engine for Neon/Postgres
# ----------------------------------------
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,           # set True for SQL debug logs
    future=True,
    pool_pre_ping=True 
)

# ----------------------------------------
# Async session factory
# ----------------------------------------
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# ----------------------------------------
# Create schema if it doesn't exist
# ----------------------------------------
async def init_db():
    """
    Ensures the PostgreSQL schema (collab) exists before tables are created.
    """
    async with engine.begin() as conn:
        await conn.execute(
            text(f"CREATE SCHEMA IF NOT EXISTS {settings.DB_SCHEMA}")
        )
        # tables created later by alembic migrations
# ----------------------------------------
# Dependency for FastAPI routes
# Provides an async DB session per request
# ----------------------------------------
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from contextlib import asynccontextmanager

Base = declarative_base()

# ✅ Engine with connection pooling
engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=False,  # Disable verbose SQL logs in prod
    pool_size=10,  # number of persistent connections
    max_overflow=20,  # how many extra (temporary) connections can open if pool is full
    pool_pre_ping=True,  # ✅ check connection health before using (prevents "stale connection" errors)
)

# ✅ Factory for async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# existing get_db (used by FastAPI Depends)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# ✅ New version for manual async with usage
@asynccontextmanager
async def get_db_context():
    async with AsyncSessionLocal() as session:
        yield session

import asyncio
import sys
from pathlib import Path

# Add parent directory (/app) to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.database import engine, Base
from app.models import User, Message


async def init_db():
    async with engine.begin() as conn:
        # Drop tables (optional if you want a clean reset)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables recreated successfully.")


if __name__ == "__main__":
    asyncio.run(init_db())

import os
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Ensure test settings before importing app
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["REDIS_URL"] = "redis://localhost:6379"
os.environ["GEMINI_API_KEY"] = ""

from db.database import Base, get_db
import db.database as db_module
from db.models import Responder, ResponderRole, ResponderStatus
import uuid


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def test_db(test_engine):
    SessionTest = async_sessionmaker(test_engine, expire_on_commit=False)
    async with SessionTest() as session:
        # Seed test responders if empty
        r1 = Responder(
            id=uuid.uuid4(),
            code="R-114",
            name="A. Kumar",
            role=ResponderRole.medic,
            sector=14,
            lat=9.9312,
            lng=76.2673,
            battery=100,
            status=ResponderStatus.available,
        )
        r2 = Responder(
            id=uuid.uuid4(),
            code="R-205",
            name="D. Rao",
            role=ResponderRole.rescue,
            sector=14,
            lat=9.9180,
            lng=76.2590,
            battery=90,
            status=ResponderStatus.available,
        )
        session.add_all([r1, r2])
        await session.commit()

        yield session

        # Cleanup
        await session.rollback()

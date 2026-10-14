import os
from pathlib import Path
import socket
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from pydantic_settings import BaseSettings, SettingsConfigDict

if sys.platform == "win32":
    import asyncio
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

BACKEND_ENV_FILE = Path(__file__).parent.parent / ".env"
ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / "env"
ROOT_DOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(ROOT_ENV_FILE), str(ROOT_DOT_ENV_FILE), str(BACKEND_ENV_FILE)),
        extra="ignore",
    )
    DATABASE_URL: str = "postgresql+psycopg://zerohour:zerohour@localhost:5432/zerohour"
    REDIS_URL: str = "redis://localhost:6379"
    GEMINI_API_KEY: str = ""
    GEMMA_MODEL: str = "gemma-4-26b-a4b-it"
    GEMMA_TRIAGE_MODEL: str = "gemma-4-e2b-it"
    GEMINI_INSECURE_SKIP_VERIFY: bool = True


settings = Settings()

def _check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

# Determine effective database URL with automatic offline-first edge fallback
effective_db_url = settings.DATABASE_URL
if effective_db_url.startswith("postgresql") and any(h in effective_db_url for h in ("localhost", "127.0.0.1")):
    if not _check_port("127.0.0.1", 5432):
        print("[EDGE RESCUE] Local PostgreSQL (localhost:5432) not detected. Operating in standalone edge mode with local SQLite database (./edgerescue.db).")
        effective_db_url = "sqlite+aiosqlite:///./edgerescue.db"

_is_postgres = effective_db_url.startswith("postgresql")
_is_remote = _is_postgres and all(
    host not in effective_db_url
    for host in ("localhost", "127.0.0.1", "@postgres:", "@postgres/")
)

# prepare_threshold=None disables server-side prepared statements, required for
# Supabase's pgbouncer transaction pooler (port 6543).
_connect_args = {"prepare_threshold": None, "sslmode": "require"} if _is_remote else {}

engine = create_async_engine(effective_db_url, echo=False, connect_args=_connect_args)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        yield session


async def create_tables():
    from db import models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    from db import models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

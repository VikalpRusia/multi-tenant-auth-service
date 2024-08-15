import asyncio
import contextlib
import logging
import traceback
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config.constants import DATABASE_URL
from models.member import Member
from models.organization import Organization
from models.role import Role

logger = logging.getLogger(__name__)

class DatabaseSessionManager:

    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self.engine = create_async_engine(host, **engine_kwargs)
        self.async_session = async_sessionmaker(bind=self.engine, autocommit=False)

    async def close(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()

        self.engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self.engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.async_session is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self.async_session.begin() as conn:
            try:
                yield conn
            except Exception:
                logger.error("An unexpected error occurred: %s")
                await conn.rollback()
                raise


sessionmanager = DatabaseSessionManager(DATABASE_URL, {"echo": True})


async def get_db_session() -> AsyncSession:
    async with sessionmanager.session() as session:
        yield session

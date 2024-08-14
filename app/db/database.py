import asyncio
import contextlib
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
                await self.close()

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.async_session is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self.async_session.begin() as conn:
            try:
                yield conn
            except Exception as exception:
                print(exception)
                await conn.rollback()
                await self.close()


sessionmanager = DatabaseSessionManager(DATABASE_URL, {"echo": True})


async def get_db_session() -> AsyncSession:
    async with sessionmanager.session() as session:
        yield session

async def main():
    async for session in get_db_session():
        # If you want to add multiple objects:
        new_org = Organization(
            name='Acme Corp',
            status=1,
            personal=False,
            settings={'subscription': 'premium'},
            created_at=1699999999,
            updated_at=1699999999
        )

        new_role = Role(
            name='Manager',
            description='Manages teams and projects',
            created_at=1699999999,
            updated_at=1699999999
        )

        # new_member = Member(
        #     org_id=1,  # Assuming this is the ID of 'Acme Corp' in the 'organization' table
        #     user_id=1,  # Assuming this is the ID of 'john.doe@example.com' in the 'users' table
        #     role_id=1,  # Assuming this is the ID of 'Manager' in the 'role' table
        #     status=1,
        #     settings={'notifications': 'enabled'},
        #     created_at=1699999999,
        #     updated_at=1699999999
        # )

        # Add multiple objects to the session
        session.add_all([new_org, new_role])

if __name__ == "__main__":
    asyncio.run(main())

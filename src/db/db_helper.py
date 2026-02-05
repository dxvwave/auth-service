from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from core.config import settings


class AsyncSessionManager:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=True)
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Dependency that yields a database session and closes it after the request.
        """
        async with self.sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self):
        """Dispose of the database engine and close all connections."""
        await self.engine.dispose()


db_session_manager = AsyncSessionManager(database_url=settings.database_url)

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import exc

from app.core.config import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.database_url.unicode_string())
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise

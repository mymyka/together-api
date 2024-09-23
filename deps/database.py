from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import config
from sqlalchemy import create_engine

engine = create_async_engine(
    config.database.url,
    echo=True,
)

sync_engine = create_engine(
    config.database.sync_url,
    echo=True,
)

SessionFactory = async_sessionmaker(
    bind=engine,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

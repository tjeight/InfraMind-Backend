from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.utils.generators import get_async_database_url


# get the database url
DATABASE_URL = get_async_database_url()


# create an engine
engine = create_async_engine(
    url=DATABASE_URL,
)


# create an async session
AsyncSessionLocal = async_sessionmaker(
    class_=AsyncSession,
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


# create a dependency
async def get_database():
    async with AsyncSessionLocal() as session:
        yield session

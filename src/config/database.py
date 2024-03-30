from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config.config import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL)

async_session = sessionmaker(
    engine, class_=AsyncSession
)


async def get_async_session():
   async with async_session() as session:
       yield session

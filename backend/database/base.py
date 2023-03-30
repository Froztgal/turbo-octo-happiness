import re
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base

from config import settings


class BaseClass(object):
    @declared_attr
    def __tablename__(cls):
        return "_".join(re.findall("[A-Z][^A-Z]*", cls.__name__)).lower()


DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_db.DSN}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base(cls=BaseClass)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

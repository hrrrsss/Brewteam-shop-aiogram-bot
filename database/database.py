from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.config import settings


engine = create_async_engine(
    settings.DATABASE_URL_asyncpg,
    echo=True)


class Base(DeclarativeBase):
    pass
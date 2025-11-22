import asyncio

from database.database import engine, Base
from database.orm import Categories, Teas


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Таблица создана")

asyncio.run(create_tables())
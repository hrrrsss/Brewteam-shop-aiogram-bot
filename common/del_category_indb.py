from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session
from database.orm import Teas, Categories


async def del_category(id: int):
    async with async_session() as session:
        async with session.begin():
            try:
                await session.execute(delete(Teas).where(Teas.category_id == id))
                await session.execute(delete(Categories).where(Categories.id == id))
            except SQLAlchemyError as e:
                print("Ошибка при удалении категории", e)
                return False
    
    print("Категория удалена")
    return True
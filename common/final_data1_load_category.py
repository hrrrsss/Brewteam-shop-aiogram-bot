from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert

from database.database import async_session
from database.orm import Categories


async def final_data_load_category(data: dict):
    async with async_session() as session:
        async with session.begin():
            try:
                new_category = insert(Categories).values(
                    category_name=data["category_name"],
                    is_active = data["is_active"]
                )
                await session.execute(new_category)
            except SQLAlchemyError as e:
                print("Ошибка при добавлении категории", e)
                return "Ошибка при добавлении категории"
    return "Категория добавлена"

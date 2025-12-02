from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session
from database.orm import Teas


async def final_data_load_tea(data: dict):
    async with async_session() as session:
        async with session.begin():
            try:
                new_text = insert(Teas).values(
                    tea_name = data["tea_name"],
                    description = data["description"],
                    price = float(data["price"]),
                    stock = int(data["stock"]),
                    category_id = int(data["category_id"]),
                    image_url = data["image_url"],
                    is_active = data["is_active"]
                )
                await session.execute(new_text)
            except SQLAlchemyError as e:
                print("Ошибка при добавлении чая", e)
                return "Ошибка при добавлении чая"
    return "Новый чай добавлен"

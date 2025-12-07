from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session
from database.orm import Orders


async def insert_data_order(tg_id: int, label: str, total_price: int, data: dict):
    async with async_session() as session:
        async with session.begin():
            try:
                insert_order = Orders(
                    user_id=tg_id,
                    status="waiting",
                    label=label,
                    total_price=total_price,
                    user_name=data["user_name"],
                    address=data["address"],
                    phone=data["phone"]
                )
                session.add(insert_order)
            except SQLAlchemyError as e:
                print("Ошибка добавления заказа", e)
                return "Ошибка"
            return "Заказ добавлен."
        

async def get_last_order(tg_id: int):
    async with async_session() as session:
        order = select(Orders.id, Orders.label).where(Orders.user_id == tg_id)
        done = await session.execute(order)
        result = done.fetchall()

        return result
    

async def update_status(id: int, status: str):
    async with async_session() as session:
        async with session.begin():
            try:
                await session.execute(
                    update(Orders)
                    .where(Orders.id == id)
                    .values(status=status)
                )
            except SQLAlchemyError as e:
                print("Ошибка", SQLAlchemyError)
                return "Ошибка"

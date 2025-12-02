from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session
from database.orm import Teas


async def get_all_teas():
    async with async_session() as session:
         teas = select(Teas.id, Teas.tea_name).order_by(Teas.id)

         done = await session.execute(teas)
         result = done.fetchall()
         return result
    

async def del_tea(tea_id: int):
    async with async_session() as session:
          async with session.begin():
            try:
                await session.execute(
                    delete(Teas).where(Teas.id == tea_id)
                )
            except SQLAlchemyError as e:
                print("Ошибка при удалении", e)
                return "Ошибка во время удаления"
            
    return "Чай удален"
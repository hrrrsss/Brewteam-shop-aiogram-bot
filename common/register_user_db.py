from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session
from database.orm import Users


async def register_user_in_db(tg_id: int, usr_name: str, full_name: str):
    async with async_session() as session:
        async with session.begin():
            try:
                result = await session.execute(
                    select(Users).where(Users.telegram_id == tg_id)
                )
                existing_user = result.scalar_one_or_none()

                if existing_user:
                    print("Пользователь уже зарегестрирован")
                    return

                new_user = Users(telegram_id=tg_id, user_name = usr_name, full_name=full_name, created_at=datetime.now())
                session.add(new_user)
            except SQLAlchemyError as e:
                print("Ошибка при добавлении нового пользователя", e)


from sqlalchemy import select
from database.orm import Admins
from database.database import async_session 


async def is_admin(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Admins).where(Admins.admin_tg_id == user_id)
        )
        admin = result.scalar_one_or_none()
        return admin is not None
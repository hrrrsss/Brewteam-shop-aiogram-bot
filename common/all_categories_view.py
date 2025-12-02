from sqlalchemy import select

from database.database import async_session
from database.orm import Categories


async def view_all_categories():
    async with async_session() as session:
        result = select(Categories.id, 
                        Categories.category_name,
                        Categories.is_active).order_by(Categories.id.asc())

        done = await session.execute(result)
        result = done.fetchall()
        return result
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from database.database import async_session
from database.orm import Categories, Teas


async def get_categories():
    async with async_session() as session:
        subquery = (
            select(Teas.id).where(
                Teas.category_id == Categories.id,
                Teas.is_active.is_(True),
                Teas.stock > 0
            ).exists()
        )

        result = select(Categories.id, Categories.category_name).where(
            Categories.is_active.is_(True),
            subquery
        ).order_by(Categories.id.asc())

        done = await session.execute(result)
        result = done.fetchall()
        return result
    

async def get_teas_for_categories(id_category: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Teas)
                .where(Teas.category_id == id_category)
                .order_by(Teas.id)
            )

        return result.scalars().all()




async def create_categories_kb():
    kb_builder = InlineKeyboardBuilder()

    categories = await get_categories()

    for c in categories:
        kb_builder.row(
            InlineKeyboardButton(text=c[1], callback_data=f"category_{c[0]}"),
        )

    return kb_builder.as_markup()
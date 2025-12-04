from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, func

from database.database import async_session
from database.orm import Teas


async def create_pagination(category_id: int, page: int):
    kb_builder = InlineKeyboardBuilder()

    quantity = await count_teas(category_id)

    kb_builder.row(
        InlineKeyboardButton(text="Назад", callback_data="back"),
        InlineKeyboardButton(text=f"{page}/{quantity}", callback_data="none"),
        InlineKeyboardButton(text="Вперед", callback_data="forward"),
        InlineKeyboardButton(text=f"Добавить в корзину", callback_data="add_cart"),
        InlineKeyboardButton(text="К категориям", callback_data="catalog")
    )
    kb_builder.adjust(3,1,1)
    return kb_builder.as_markup()



async def count_teas(category_id):
    async with async_session() as session:
        result = await session.execute(
            select(func.count(Teas.id))
            .where(Teas.category_id == category_id)
        )

        count = result.scalar()
        return count
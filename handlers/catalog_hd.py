from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.users_kb.catalog_category_kb import create_categories_kb


catalog_router = Router()


@catalog_router.callback_query(F.data == "catalog")
async def catalog_cb(callback: CallbackQuery):
    keyboard = await create_categories_kb()

    await callback.message.edit_text(
        text="Выберите категорию чая",
        reply_markup=keyboard
    )
from aiogram import Router, F
from aiogram.types import CallbackQuery


catalog_router = Router()


@catalog_router.callback_query(F.data == "catalog")
async def catalog_cb(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите категорию чая",
        reply_markup=...
    )
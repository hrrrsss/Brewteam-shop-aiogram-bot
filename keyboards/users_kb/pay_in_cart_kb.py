from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def pay_in_cart():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(text="📑Оформить заказ", callback_data='order'),
        InlineKeyboardButton(text="Вернуться", callback_data="catalog")
    )
    kb_builder.adjust(1, 1)

    return kb_builder.as_markup()
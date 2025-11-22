from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_mainmenu_kb():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(text="🍃Каталог", callback_data='catalog'),
        InlineKeyboardButton(text="🛒Корзина", callback_data='cart'),
        InlineKeyboardButton(text="📑Оформить заказ", callback_data='order'),
        InlineKeyboardButton(text="ℹ️О магазине", callback_data='about_shop')
    )
    kb_builder.adjust(2, 2)

    return kb_builder.as_markup()
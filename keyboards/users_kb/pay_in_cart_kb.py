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


def enter_data_user():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(text="Ввести данные", callback_data="order_data")
    )

    return kb_builder.as_markup()


def link_for_pay(url: str):
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(text="Оплата заказа", url=url)
    )

    return kb_builder.as_markup()


def check_pay():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(text="Проверить оплату", callback_data="check_payment")
    )
    return kb_builder.as_markup()
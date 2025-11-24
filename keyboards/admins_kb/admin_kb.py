from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_kb():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(text="Изменение категорий", callback_data="admin_category"),
        InlineKeyboardButton(text="Изменение товаров", callback_data="admin_product"),
        InlineKeyboardButton(text="Заказы", callback_data="admin_order"),
        InlineKeyboardButton(text="Рассылка", callback_data="admin_mailing"),
        InlineKeyboardButton(text="Статистика", callback_data="admin_statistics"),
        InlineKeyboardButton(text="Пользователи", callback_data="admin_users"),
        )
    kb_builder.adjust(1, 1, 1, 1, 1, 1)

    return kb_builder.as_markup()
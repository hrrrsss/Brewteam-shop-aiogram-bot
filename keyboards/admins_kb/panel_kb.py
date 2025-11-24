from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.users_kb.catalog_category_kb import get_categories



#Клавиатуры для категорий:

async def create_admin_category_kb():
    kb_builder = InlineKeyboardBuilder()

    categories = await get_categories()

    all_categories = [f"{c[0]}.{c[1]}" for c in categories]

    buttons = [InlineKeyboardButton(text=str(c[0]), callback_data=f"del_category_{c[0]}") for c in categories]

    kb_builder.row(*buttons, width=3)


    return all_categories, kb_builder.as_markup()


def create_admin_choice_action_category():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text="Добавить новую категорию", callback_data="admin_category_add"),
                   InlineKeyboardButton(text="Удалить существующую категорию", callback_data="admin_category_del"),
                   InlineKeyboardButton(text="Сделать активной или неактивной существующую категорию", callback_data="admin_category_nonactive"))
    kb_builder.adjust(1, 1, 1)

    return kb_builder.as_markup()


def create_admin_choice_isactive_or_no():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text="Активная", callback_data="active"),
                   InlineKeyboardButton(text="Неактивная", callback_data="nonactive"))
    
    kb_builder.adjust(1, 1)
    
    return kb_builder.as_markup()
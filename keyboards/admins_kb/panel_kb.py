from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.users_kb.catalog_category_kb import get_categories
from common.all_categories_view import view_all_categories
from common.get_del_all_teas import get_all_teas


#Клавиатуры для продуктов:

def create_admin_choice_tea_isactive_or_no():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text="Активная", callback_data="tea_active"),
                   InlineKeyboardButton(text="Неактивная", callback_data="tea_nonactive"))
    
    kb_builder.adjust(1, 1)
    
    return kb_builder.as_markup()


async def create_admin_add_id_category_for_tea():
    kb_builder = InlineKeyboardBuilder()

    categories = await get_categories()

    all_categories = [f"{c[0]}.{c[1]}" for c in categories]

    buttons = [InlineKeyboardButton(text=str(c[0]), callback_data=f"choice_category_{c[0]}") for c in categories]

    kb_builder.row(*buttons, width=3)


    return all_categories, kb_builder.as_markup()


async def create_admin_all_teas_del():
    kb_builder = InlineKeyboardBuilder()

    teas = await get_all_teas()

    all_teas = [f"{t[0]}.{t[1]}" for t in teas]
    buttons = [InlineKeyboardButton(text=str(t[0]), callback_data=f"del_teas_{t[0]}") for t in teas]

    kb_builder.row(*buttons, width=3)

    return all_teas, kb_builder.as_markup()


def create_admin_products():
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text="Добавить новый чай", callback_data="new_tea"),
                   InlineKeyboardButton(text="Удалить существующий чай", callback_data="drop_tea"))
    return kb_builder.as_markup()



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


async def create_admin_all_categories():
    kb_builder = InlineKeyboardBuilder()

    categories = await view_all_categories()

    buttons = [InlineKeyboardButton(text=f"{c[1]} - {'активна' if c[2] else 'неактивна'}", 
                                    callback_data=f"active_{c[2]}_{c[0]}") for c in categories]

    kb_builder.row(*buttons, width=1)


    return kb_builder.as_markup()
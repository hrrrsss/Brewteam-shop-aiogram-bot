from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.help_func.admin_check import is_admin
from keyboards.admins_kb import admin_kb, panel_kb
from common.del_category_indb import del_category
from common.final_data1_load_category import final_data_load_category


admin_router = Router()

class AddCategory(StatesGroup):
    category_name = State()
    is_active = State()


@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    if not await is_admin(message.from_user.id):
        return
    
    await message.answer("Добро пожаловать в админ панель магазин BrewTeam", reply_markup=admin_kb.admin_kb())


@admin_router.callback_query((F.data == "admin_category_nonactive") | (F.data == "admin_category_del") | (F.data == "admin_category_add"))
async def admin_add_or_del_category(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        return

    if callback.data == "admin_category_add":
        await callback.message.answer(text="Введите название категории")
        await state.set_state(AddCategory.category_name)
    elif callback.data == "admin_category_del":
        result_func = await panel_kb.create_admin_category_kb()
        ret_text = '\n'.join(result_func[0])
        await callback.message.edit_text(text=(f"<b>Учитывайте, что при переключении категории будут удалены и все чаи в этой категории</b>\n\n"
                                               f"Выберите категорию которую хотите удалить:\n\n{ret_text}"), 
                                               reply_markup=result_func[1])
    elif callback.data == "admin_category_nonactive":
        await callback.message.edit_text(text="неактив")


@admin_router.message(AddCategory.category_name, F.text)
async def add_name(message: Message, state: FSMContext):
    if len(message.text) < 1 or len(message.text) > 100:
        await message.answer("Название категории должно быть больше 1 символа и меньше 100 символов")
        return
    await state.set_data({"category_name": message.text})
    await message.answer("Категория должна быть уже активной или нет?", reply_markup=panel_kb.create_admin_choice_isactive_or_no())
    await state.set_state(AddCategory.is_active)


@admin_router.callback_query(AddCategory.is_active)
async def add_is_active(callback: CallbackQuery, state: FSMContext):
    is_active = False
    if callback.data == "active":
        is_active = True
    await state.update_data({"is_active": is_active})
    await callback.message.answer("Категория добавляется...")
    data = await state.get_data()
    await state.clear()
    final_text = await final_data_load_category(data)
    await callback.message.answer(final_text)


@admin_router.callback_query(F.data.startswith("del_category"))
async def admin_del_category(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        return
    
    id_find = callback.data[callback.data.rfind("_")+1:]
    result = await del_category(int(id_find))
    if result:
        await callback.message.edit_text(text="Категория удалена")
    else:
        await callback.message.edit_text(text="Ошибка при удалении категории")


#ГЛАВНЫЙ ХЕНДЛЕР
@admin_router.callback_query(F.data.startswith("admin"))
async def admin_callback(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        return

    if callback.data == "admin_category":
        await callback.message.edit_text(text="Выберите действие", reply_markup=panel_kb.create_admin_choice_action_category())
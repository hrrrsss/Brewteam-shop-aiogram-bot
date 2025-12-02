from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.help_func.admin_check import is_admin
from keyboards.admins_kb import admin_kb, panel_kb
from common.del_category_indb import del_category
from common.final_data1_load_category import final_data_load_category
from common.change_active import change_active_category
from common.final_data1_load_tea import final_data_load_tea
from common.get_del_all_teas import del_tea


admin_router = Router()

class AddCategory(StatesGroup):
    category_name = State()
    is_active = State()


class AddTea(StatesGroup):
    tea_name = State()
    description = State()
    price = State()
    stock = State()
    category_id = State()
    image = State()
    is_active = State()


@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    if not await is_admin(message.from_user.id):
        return
    
    await message.answer("Добро пожаловать в админ панель магазин BrewTeam", reply_markup=admin_kb.admin_kb())


@admin_router.message(F.text == 'отмена')
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено")


#ХЕНДЛЕРЫ ДЛЯ КАТЕГОРИЙ
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
        await callback.message.edit_text(text=(f"<b>Учитывайте, что при удалении категории будут удалены и все чаи в этой категории</b>\n\n"
                                               f"Выберите категорию которую хотите удалить:\n\n{ret_text}"), 
                                               reply_markup=result_func[1])
    elif callback.data == "admin_category_nonactive":
        await callback.message.edit_text(text=("<b>Учитывайте, что изменение состояния сказывается и на отключении чаев.</b>\n\n"
                                               "Выберите категорию, которая должна изменить состояние"),
                                               reply_markup= await panel_kb.create_admin_all_categories())


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
    callback.message.edit_text(text=result)


@admin_router.callback_query(F.data.startswith("active"))
async def admin_active_off_on(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        return
    
    result = await change_active_category(callback.data)
    await callback.message.delete()
    await callback.answer(result, show_alert=True)


#ХЕНДЛЕРЫ ДЛЯ ЧАЕВ
@admin_router.callback_query((F.data == "new_tea") | (F.data == "drop_tea"))
async def admin_change_tea(callback: CallbackQuery, state: FSMContext):
    if callback.data == "new_tea":
        await callback.message.edit_text(text="Введите название чая")
        await state.set_state(AddTea.tea_name)
    else:
        result_func = await panel_kb.create_admin_all_teas_del()
        teas = "\n".join(result_func[0])
        await callback.message.edit_text(f"Выберите чай для удаления:\n\n{teas}", reply_markup=result_func[1])


@admin_router.message(AddTea.tea_name, F.text)
async def admin_add_tea_name(message: Message, state: FSMContext):
    await state.set_data({"tea_name": message.text})
    await message.answer("Введите описание")
    await state.set_state(AddTea.description)


@admin_router.message(AddTea.description, F.text)
async def admin_add_tea_descrip(message: Message, state: FSMContext):
    await state.update_data({"description": message.text})
    await message.answer("Введите цену")
    await state.set_state(AddTea.price)


@admin_router.message(AddTea.price, F.text)
async def admin_add_tea_price(message: Message, state: FSMContext):
    await state.update_data({"price": message.text})
    await message.answer("Введите кол-во на складе")
    await state.set_state(AddTea.stock)


@admin_router.message(AddTea.stock, F.text)
async def admin_add_tea_stock(message: Message, state: FSMContext):
    await state.update_data({"stock": message.text})

    result_func = await panel_kb.create_admin_add_id_category_for_tea()
    ret_text = '\n'.join(result_func[0])

    await message.answer(f"Выберите к какой категории будет относится чай:\n\n{ret_text}", reply_markup=result_func[1])
    await state.set_state(AddTea.category_id)


@admin_router.callback_query(AddTea.category_id)
async def admin_add_tea_catregory_id(callback: CallbackQuery, state: FSMContext):
    id_find = int(callback.data[callback.data.rfind("_")+1:])
    await state.update_data({"category_id": id_find})
    await callback.message.edit_text(text="Отправьте url картинки")
    await state.set_state(AddTea.image)


@admin_router.message(AddTea.image, F.text)
async def admin_add_tea_image(message: Message, state: FSMContext):
    await state.update_data({"image_url": message.text})
    await message.answer("Чай будет активен или нет?", reply_markup=panel_kb.create_admin_choice_tea_isactive_or_no())
    await state.set_state(AddTea.is_active)


@admin_router.callback_query(AddTea.is_active)
async def admin_add_tea_is_active(callback: CallbackQuery, state: FSMContext):
    is_active = False
    if callback.data == "tea_active":
        is_active = True
    await state.update_data({"is_active": is_active})
    data = await state.get_data()
    await state.clear()
    result = await final_data_load_tea(data)
    await callback.message.answer(result)


@admin_router.callback_query(F.data.startswith("del_teas"))
async def admin_del_tea(callback: CallbackQuery):
    id_find = int(callback.data[callback.data.rfind("_")+1:])
    print(id_find)
    result_func = await del_tea(id_find)
    await callback.message.answer(result_func)


#ГЛАВНЫЙ ХЕНДЛЕР
@admin_router.callback_query(F.data.startswith("admin"))
async def admin_callback(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        return

    if callback.data == "admin_category":
        await callback.message.edit_text(text="Выберите действие", reply_markup=panel_kb.create_admin_choice_action_category())
    elif callback.data == "admin_product":
        await callback.message.edit_text(text="Выберите действие", reply_markup=panel_kb.create_admin_products())
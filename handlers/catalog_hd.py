from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.users_kb.catalog_category_kb import create_categories_kb, get_teas_for_categories
from keyboards.users_kb.pagination_kb import create_pagination
from common.add_tea_in_cart import add_tea_in_cart


catalog_router = Router()


class PaginationTeas(StatesGroup):
    category = State()
    teas = State()


@catalog_router.callback_query(F.data == "catalog")
async def catalog_cb(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()

    keyboard = await create_categories_kb()

    await callback.message.answer(
        text="Выберите категорию чая",
        reply_markup=keyboard
    )

    await state.set_state(PaginationTeas.category)


@catalog_router.callback_query(PaginationTeas.category, F.data.startswith("category"))
async def teas_cb(callback: CallbackQuery, state: FSMContext):
    id_category = int(callback.data[callback.data.rfind("_")+1:])
    result = await get_teas_for_categories(id_category)

    await state.set_data({"category": id_category})
    await state.update_data({"page": 1})

    teas_data = [{"id": int(t.id), 
                  "tea_name": t.tea_name, 
                  "description": t.description, 
                  "price": float(t.price),
                  "image_url": t.image_url} for t in result]
    await state.update_data({"teas": teas_data})
    
    text=f"<b>{result[0].tea_name}</b>\n{result[0].description}\n\nЦена: {result[0].price} рублей"
    media = InputMediaPhoto(media=result[0].image_url, caption=text)
    await callback.message.edit_media(
        media=media,
        reply_markup=await create_pagination(id_category, 1)
    )
    await state.set_state(PaginationTeas.teas)



@catalog_router.callback_query(PaginationTeas.teas, F.data == "forward")
async def teas_forward(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data["page"]
    if page < len(data["teas"]):
        page += 1
        await state.update_data({"page": page})
        for_send = data["teas"][page-1]
        text=f"<b>{for_send['tea_name']}</b>\n{for_send['description']}\n\nЦена: {for_send['price']} рублей"
        media = InputMediaPhoto(media=for_send["image_url"], caption=text)

        await callback.message.edit_media(
            media=media,
            reply_markup=await create_pagination(data["category"], page)
        )



@catalog_router.callback_query(PaginationTeas.teas, F.data == "back")
async def teas_back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data["page"]
    if page > 1:
        page -= 1
        await state.update_data({"page": page})
        for_send = data["teas"][page-1]
        text=f"<b>{for_send['tea_name']}</b>\n{for_send['description']}\n\nЦена: {for_send['price']} рублей"
        media = InputMediaPhoto(media=for_send["image_url"], caption=text)

        await callback.message.edit_media(
            media=media,
            reply_markup=await create_pagination(data["category"], page)
        )


@catalog_router.callback_query(F.data == "add_cart")
async def teas_cart(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data["page"]
    id_tea = int(data["teas"][page-1]["id"])
    
    result = await add_tea_in_cart(int(callback.from_user.id), id_tea)
    await callback.answer(result)
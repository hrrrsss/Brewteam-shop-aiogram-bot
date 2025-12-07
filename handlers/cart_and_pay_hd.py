from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from common import view_cart, order_add_db
from keyboards.users_kb.pay_in_cart_kb import (pay_in_cart, 
                                               enter_data_user, 
                                               link_for_pay, 
                                               check_pay)
from services.youmoney import pay_yoomoney


cart_router = Router()


class OrderData(StatesGroup):
    name = State()
    address = State()
    phone = State()



@cart_router.callback_query(F.data == "cart")
async def cart_user(callback: CallbackQuery):
    id = int(callback.from_user.id)
    user_cart = await view_cart.view_cart(id)
    text = "\n\n".join([f"-<b>{i}</b> - {user_cart[i][1]} шт. - <i>{user_cart[i][0]} рублей</i>" for i in user_cart])
    total_price = sum([i[0] for i in user_cart.values()])
    text += f"\n\n<b>Итоговая сумма: {total_price} рублей</b>"

    await callback.message.edit_text(
        text=text,
        reply_markup=pay_in_cart()
    )


@cart_router.callback_query(F.data == "order")
async def order_user(callback: CallbackQuery):
    id = int(callback.from_user.id)
    user_cart = await view_cart.view_cart(id)
    text = "\n\n".join([f"-<b>{i}</b> - {user_cart[i][1]} шт. - <i>{user_cart[i][0]} рублей</i>" for i in user_cart])
    total_price = sum([i[0] for i in user_cart.values()])
    text += f"\n\n<b>Итоговая сумма: {total_price} рублей</b>\n\nВведите данные для оформления заказа"

    await callback.message.edit_text(
        text=text,
        reply_markup=enter_data_user()
    )


@cart_router.callback_query(F.data == "order_data")
async def order_data_enter(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваше имя")
    await state.set_state(OrderData.name)


@cart_router.message(OrderData.name)
async def order_name(message: Message, state: FSMContext):
    if len(message.text) < 2 and len(message.text) > 30:
        await message.answer("Введите корректное имя")
        return
    await state.set_data({"user_name": message.text})
    await message.answer("Введите адрес для получения товара")
    await state.set_state(OrderData.address)


@cart_router.message(OrderData.address)
async def order_address(message: Message, state: FSMContext):
    await state.update_data({"address": message.text})
    await message.answer("Введите номер телефона")
    await state.set_state(OrderData.phone)


@cart_router.message(OrderData.phone)
async def order_phone(message: Message, state: FSMContext):
    id = int(message.from_user.id)
    user_cart = await view_cart.view_cart(id)
    total_price = sum([i[0] for i in user_cart.values()])

    await state.update_data({"phone": message.text})
    data = await state.get_data()

    link, label = pay_yoomoney(str(id), total_price)

    result_func = await order_add_db.insert_data_order(id, label, total_price, data)
    await message.answer(result_func)

    await message.answer("Оплатите заказ", reply_markup=link_for_pay(link))

    await message.answer(
        "Когда оплатите — нажмите кнопку ниже",
        reply_markup=check_pay()
    )

    await state.clear()


@cart_router.message(F.data == "check_payment")
async def check_pay(callback: CallbackQuery):
    user_id = callback.from_user.id

    order = await order_add_db.get_last_order(user_id)

    if not order:
        await callback.message.answer("Заказ не найден")
        return
    
    label = order["label"]

    from services.youmoney import check_yoomoney
    paid = check_yoomoney(label)

    if paid:
        await order_add_db.update_status(order["id"], "paid")
        await callback.message.answer("✅ Оплата подтверждена! Заказ передан на сборку.")
    else:
        await callback.message.answer("❌ Оплата пока не найдена. Попробуйте позже.")
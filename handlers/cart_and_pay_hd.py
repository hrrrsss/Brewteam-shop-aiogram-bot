from aiogram import Router, F
from aiogram.types import CallbackQuery

from common.view_cart import view_cart
from keyboards.users_kb.pay_in_cart_kb import pay_in_cart


cart_router = Router()


@cart_router.callback_query(F.data == "cart")
async def cart_user(callback: CallbackQuery):
    id = int(callback.from_user.id)
    user_cart = await view_cart(id)
    text = "\n\n".join([f"-<b>{i}</b> - {user_cart[i][1]} шт. - <i>{user_cart[i][0]} рублей</i>" for i in user_cart])
    total_price = sum([i[0] for i in user_cart.values()])
    text += f"\n\n<b>Итоговая сумма: {total_price} рублей</b>"

    await callback.message.edit_text(
        text=text,
        reply_markup=pay_in_cart()
    )
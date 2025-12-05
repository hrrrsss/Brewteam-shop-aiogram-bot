from sqlalchemy import select

from database.database import async_session
from database.orm import Users, Teas, Cart


async def view_cart(tg_id: int):
    async with async_session() as session:
        result = select(Users.id).where(Users.telegram_id == tg_id)
        done = await session.execute(result)
        user_id = done.scalar_one()

        result = select(Cart.tea_id, Cart.quantity).where(Cart.user_id == user_id)
        done = await session.execute(result)
        cart_data = done.fetchall()

        name_price_tea = []
        for tea in cart_data:
            result = select(Teas.tea_name, Teas.price).where(Teas.id == tea[0])
            done = await session.execute(result)
            name_price_tea.append(done.fetchall()[0])

        result = {}
        for num in range(len(cart_data)):
            result[name_price_tea[num][0]] = (int(name_price_tea[num][1]), cart_data[num][1])

        return result


from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session
from database.orm import Cart, Users


async def add_tea_in_cart(user_id: int, tea_id: int):
    async with async_session() as session:
        async with session.begin():
            try:
                user = await session.execute(select(Users.id).where(Users.telegram_id == user_id))
                user_id_db = user.scalar_one()

                count = await how_much_tea_in_cart(user_id_db, tea_id)

                if count == 0:
                    new_tea = Cart(
                        user_id=user_id_db,
                        tea_id=tea_id,
                        quantity=1
                    )
                    session.add(new_tea)
                else:
                    upd_quan = update(Cart).where(Cart.user_id == user_id_db,
                                                  Cart.tea_id == tea_id).values(quantity=Cart.quantity+1)
                    await session.execute(upd_quan)
            except SQLAlchemyError as e:
                print("Ошибка добавления чая в корзину", e)

    if count > 0:
        return f"Чай добавлен в корзину (кол-во - {count+1})"
    else:
        return "Чай добавлен"
        


async def how_much_tea_in_cart(user_id: int, tea_id: int):
    async with async_session() as session:
        check_quantity = await session.execute(
            select(Cart.id).where(Cart.user_id == user_id,
                                  Cart.tea_id == tea_id)
        )
        if check_quantity.scalar_one_or_none():
            quantity_req = await session.execute(
                select(Cart.quantity).where(Cart.tea_id == tea_id)
            )
            quantity = quantity_req.scalar()
            return quantity
        return 0

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session
from database.orm import Teas, Categories


async def change_active_category(data: str):
    first_ = data.find('_')+1
    second_ = data.rfind('_')
    state = data[first_:second_]
    if state == 'True':
        state = False
    else:
        state = True

    id = int(data[second_+1:])

    async with async_session() as session:
        try:
            async with session.begin():
                    update_category = (
                        update(Categories)
                        .where(Categories.id == id)
                        .values(is_active=state)
                    )
                    update_teas = (
                        update(Teas)
                        .where(Teas.category_id == id)
                        .values(is_active=state)
                    )
                    await session.execute(update_category)
                    await session.execute(update_teas)
        except SQLAlchemyError as e:
            print("ошибка", e)
            return "Ошибка при изменении состояния"
    
    return "Состояние изменено"
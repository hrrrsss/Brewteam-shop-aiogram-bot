import asyncio

import logging
from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import settings
from handlers import cart_and_pay_hd, start_hd, catalog_hd, admin_hd
from keyboards.users_kb.menu_kb import set_main_menu


logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.getLevelName(level=settings.log_level),
        format=settings.log_format,
    )
    logger.info("Starting bot")

    r = Redis(host='localhost', port=6379, db=0)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=RedisStorage(redis=r))


    await set_main_menu(bot)


    dp.include_router(start_hd.start_router)
    dp.include_router(admin_hd.admin_router)
    dp.include_router(catalog_hd.catalog_router)
    dp.include_router(cart_and_pay_hd.cart_router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from lexicon.lexicon import LEXICON
from keyboards.users_kb.main_menu_kb import create_mainmenu_kb
from database.help_func.admin_check import is_admin
from common.register_user_db import register_user_in_db


start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(message: Message):
    await register_user_in_db(int(message.from_user.id), 
                        message.from_user.username, 
                        message.from_user.full_name)
    await message.answer(LEXICON['start'], reply_markup=create_mainmenu_kb())


@start_router.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer(LEXICON['help'])


@start_router.callback_query(F.data == "about_shop")
async def about_cmd(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON['about'])
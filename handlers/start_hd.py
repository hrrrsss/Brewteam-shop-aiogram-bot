from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from lexicon.lexicon import LEXICON
from keyboards.main_menu_kb import create_mainmenu_kb


start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(LEXICON['start'], reply_markup=create_mainmenu_kb())


@start_router.message(Command('help'))
async def about_cmd(message: Message):
    await message.answer(LEXICON['help'])
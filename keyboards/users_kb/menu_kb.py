from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from lexicon.lexicon import LEXICON_MENU


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=k, description=v)
        for k, v in LEXICON_MENU.items()
    ]
    await bot.set_my_commands(
        commands=main_menu_commands,
        scope=BotCommandScopeAllPrivateChats()
    )
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from bot_info import DP
from constants import TEXT
from handlers.users.menu import menu


@DP.message_handler(CommandHelp())
async def command_help(message: types.Message):
    global TEXT
    await message.answer(TEXT.general_rules())
    await menu(message)

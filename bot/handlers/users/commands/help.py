from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from bot_info import DP
from constants import TEXT
from handlers.users.menu import menu


@DP.message_handler(CommandHelp())
async def command_help(message: types.Message):
    """The handler for the 'help' command for the general rules of using"""
    global TEXT
    await message.answer(TEXT().general_rules())
    await menu(message)

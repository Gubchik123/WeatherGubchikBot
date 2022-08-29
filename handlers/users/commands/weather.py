from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from ..info_choosing import choosing_region


@DP.message_handler(commands="weather")
async def command_weather(message: types.Message):
    await choosing_region(message, "normal")

from aiogram import types

from bot_info import DP
from constants import TEXT
from keyboard import make_keyboard_for_country_choosing


@DP.message_handler(commands="weather")
async def command_weather(message: types.Message) -> None:
    """The handler for the 'weather' command"""
    await message.answer(
        TEXT().choose_weather_country_question_message(),
        reply_markup=make_keyboard_for_country_choosing(),
    )

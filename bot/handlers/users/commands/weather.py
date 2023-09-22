from aiogram import types

from bot_info import DP
from constants import TEXT
from ..info_choosing import weather_forecast


@DP.message_handler(commands="weather")
async def command_weather(message: types.Message) -> None:
    """The handler for the 'weather' command"""
    message.text = {  # ! Workaround
        "ua": "прогноз погоди",
        "ru": "прогноз погоды",
        "en": "weather forecast",
    }.get(TEXT().lang_code)
    await weather_forecast(message)

import asyncio

from aiogram.types import Message, FSInputFile

from handlers.users.menu import handle_menu
from utils.db.crud.search_log import create_search_log
from utils.weather.general import send_message_to_user_about_error
from utils.weather.graph import get_generated_temp_graph_image_path
from utils.weather.parsing import (
    INFO,
    MAX_TEMPS,
    MIN_TEMPS,
    get_information_about_one_day,
    get_information_about_many_days,
)


async def send_weather_forecast_by_(message: Message, data: dict):
    """Sends weather forecast to user (creates search log)."""
    await _send_weather_forecast_by_(message, data)
    asyncio.create_task(create_search_log(message.chat.id, data["city_title"]))


async def _send_weather_forecast_by_(message: Message, data: dict):
    """Sends weather forecast to user."""
    INFO.set(**data)

    try:
        send_function = (
            _send_weather_forecast_for_one_day
            if INFO.about_one_day
            else _send_weather_forecast_for_many_days
        )
        await send_function(message)
        await handle_menu(message)
    except Exception as error:
        await send_message_to_user_about_error(
            message, str(error), error_place=" during parsing"
        )


async def _send_weather_forecast_for_one_day(message: Message):
    """Sends weather forecast for one day."""
    await message.answer(get_information_about_one_day(), parse_mode="HTML")


async def _send_weather_forecast_for_many_days(message: Message):
    """Sends weather forecast for many days."""
    await message.answer(get_information_about_many_days(), parse_mode="HTML")
    await message.answer_photo(
        FSInputFile(get_generated_temp_graph_image_path(MAX_TEMPS, MIN_TEMPS))
    )

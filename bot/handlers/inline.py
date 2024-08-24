import asyncio
from types import ModuleType

from aiogram import Router, F, types

from utils.admins import send_to_admins

from .users.weather.from_command import (
    is_command_arguments_valid_,
    get_error_message_by_,
)


inline_router = Router()


@inline_router.inline_query(F.query.strip().split().len() == 4)
async def handle_inline_query(inline_query: types.InlineQuery):
    """Handles inline query to process like the weather command with args."""
    result = await is_command_arguments_valid_(
        inline_query.query, check_length=False
    )
    if isinstance(result, ModuleType):
        await _send_weather_forecast(inline_query, result)
        asyncio.create_task(
            send_to_admins(
                "ℹ️ Someone got weather through inline query in "
                f"{result.INFO.city_title} ({result.INFO.time_title})."
            )
        )
        return
    await _send_error_message(inline_query, error_key=result)


async def _send_weather_forecast(
    inline_query: types.InlineQuery, weather_provider_module: ModuleType
):
    """Sends the weather forecast to the inline query."""
    if weather_provider_module.INFO.about_now:
        get_function = weather_provider_module.get_information_for_now
    elif weather_provider_module.INFO.about_one_day:
        get_function = weather_provider_module.get_information_about_one_day
    else:
        get_function = weather_provider_module.get_information_about_many_days

    weather_forecast = get_function()

    await inline_query.answer(
        [
            types.InlineQueryResultArticle(
                id="1",
                title=weather_forecast.split("\n\n")[0],
                input_message_content=types.InputTextMessageContent(
                    message_text=weather_forecast
                ),
            )
        ]
    )


async def _send_error_message(inline_query: types.InlineQuery, error_key: str):
    """Sends the error message to the inline query."""
    error_key = get_error_message_by_(error_key)
    await inline_query.answer(
        [
            types.InlineQueryResultArticle(
                id="1",
                title=error_key,
                input_message_content=types.InputTextMessageContent(
                    message_text=error_key
                ),
            )
        ]
    )

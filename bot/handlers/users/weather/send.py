import asyncio
from types import ModuleType

from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, FSInputFile

from handlers.users.menu import handle_menu
from utils.error import send_message_about_error
from utils.db.crud.user import get_user_by_
from utils.db.crud.search_log import create_search_log
from utils.weather import get_weather_provider_module_by_
from utils.weather.request import WeatherProviderServerError
from utils.weather.graph import get_generated_temp_graph_image_path


async def send_weather_forecast_by_(message: Message, data: dict):
    """Sends weather forecast to user (creates search log)."""
    await _send_weather_forecast_by_(message, data)
    asyncio.create_task(
        create_search_log(
            message.chat.id, data["city_title"], data["lang_code"]
        )
    )


async def _send_weather_forecast_by_(message: Message, data: dict):
    """Sends weather forecast to user."""
    user = get_user_by_(message.chat.id)
    weather_provider_module = get_weather_provider_module_by_(
        user.weather_provider
    )
    weather_provider_module.INFO.set(**data)

    try:
        send_function = (
            _send_weather_forecast_for_one_day
            if weather_provider_module.INFO.about_one_day
            else _send_weather_forecast_for_many_days
        )
        await send_function(message, weather_provider_module)
        await handle_menu(message)
    except WeatherProviderServerError as error:
        await message.answer(
            _(
                "Unfortunately, the weather provider server is not available now. "
                "The error is not connected with the bot. Please, try again later."
            )
        )
        await send_message_about_error(
            message,
            str(error),
            error_place=f" {str(error.__class__)[8:-2]}",
            message_to_user=False,
        )
    except Exception as error:
        await send_message_about_error(
            message, str(error), error_place=f" {str(error.__class__)[8:-2]}"
        )


async def _send_weather_forecast_for_one_day(
    message: Message, weather_provider_module: ModuleType
):
    """Sends weather forecast for one day."""
    await message.answer(
        weather_provider_module.get_information_about_one_day(),
        parse_mode="HTML",
    )


async def _send_weather_forecast_for_many_days(
    message: Message, weather_provider_module: ModuleType
):
    """Sends weather forecast for many days."""
    await message.answer(
        weather_provider_module.get_information_about_many_days(),
        parse_mode="HTML",
    )
    await message.answer_photo(
        FSInputFile(
            get_generated_temp_graph_image_path(
                weather_provider_module.MAX_TEMPS,
                weather_provider_module.MIN_TEMPS,
            )
        )
    )

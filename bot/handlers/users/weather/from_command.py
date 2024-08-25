import asyncio
from types import ModuleType
from typing import Union, Optional, Dict

from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from utils.admins import send_to_admins
from utils.weather import get_weather_provider_module_by_
from data.config import ADMINS, WEATHER_PROVIDERS, LANGUAGES

from .send import send_weather_forecast_with_


async def handle_weather_command_with_arguments(message: Message):
    """Handles the /weather command with arguments."""
    result = await is_weather_command_arguments_valid_(message.text.strip())

    if isinstance(result, ModuleType):
        await send_weather_forecast_with_(message, result)
        if message.chat.id not in ADMINS:
            asyncio.create_task(
                send_to_admins(
                    f"ℹ️ '{message.chat.title or message.from_user.full_name}' "
                    f"{message.chat.type} "
                    f"(<code>{message.chat.id}</code>) got weather in "
                    f"{result.INFO.city_title} ({result.INFO.time_title})."
                )
            )
        return
    await message.answer(_get_weather_error_message_by_(result))


async def is_weather_command_arguments_valid_(
    command: str, check_length: Optional[bool] = True
) -> Union[ModuleType, str]:
    """Checks if the /weather command arguments is valid
    and returns the error message key if it's not valid."""
    if check_length:
        args = command.strip().split(" ")[1:]
        if len(args) != 4:
            return "length"
    else:
        args = command.strip().split(" ")
    language, weather_provider, city, period = args
    # Check language
    if language not in LANGUAGES:
        return "language"
    # Check weather provider
    if weather_provider not in WEATHER_PROVIDERS:
        return "weather_provider"

    weather_provider_module = get_weather_provider_module_by_(weather_provider)
    # Check city
    result_city, is_city_match_100 = (
        await weather_provider_module.get_searched_data_with_(
            city.lower(), language
        )
    )
    if not is_city_match_100:
        return "city"
    # Check period
    time = weather_provider_module.INFO.get_time_by_(period)
    if time is None:
        return "period"

    weather_provider_module.INFO.set(
        **{
            "city": result_city,
            "city_title": city.capitalize(),
            "time": time,
            "time_title": period,
            "lang_code": language,
            "type": "weather" if time != "review" else time,
        }
    )
    return weather_provider_module


def _get_weather_error_message_by_(error: str) -> str:
    """Returns weather error message by the given error message key."""
    return get_weather_error_messages().get(error)


def get_weather_error_messages() -> Dict[str, str]:
    """Returns all error messages for the /weather command arguments."""
    return {
        "length": _(
            "❌ Invalid number of arguments. Expected 4 arguments: "
            "[language code: {languages}] [weather provider: {providers}] "
            "[city] [period]"
        ).format(
            languages=", ".join(LANGUAGES),
            providers=", ".join(WEATHER_PROVIDERS),
        ),
        "language": _(
            "❌ Unknown language code. Expected one of: {languages}"
        ).format(languages=", ".join(LANGUAGES)),
        "weather_provider": _(
            "❌ Unknown weather provider. Expected one of: {providers}"
        ).format(providers=", ".join(WEATHER_PROVIDERS)),
        "city": _("❌ Exact city not found. Fuzzy search is not allowed."),
        "period": _("❌ Invalid period."),
    }

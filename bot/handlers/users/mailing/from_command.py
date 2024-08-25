import asyncio
from types import ModuleType
from datetime import datetime
from typing import Union, Optional, NamedTuple

from pytz import timezone as tz
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.admins import send_to_admins
from utils.scheduler import send_mailing
from utils.weather import get_weather_provider_module_by_
from utils.db.models import User
from utils.db.crud.mailing import get_mailing_by_, create_mailing_for_
from utils.db.crud.user import get_user_by_, create_user_by_, delete_user_with_
from data.config import (
    ADMINS,
    DEFAULT_TIMEZONE,
    WEATHER_PROVIDERS,
    LANGUAGES,
    MAILING_TIMES,
)

from ..weather.from_command import get_weather_error_messages

from .unsubscribe import remove_mailing_for_


async def handle_mailing_command_with_arguments(
    message: Message, scheduler: AsyncIOScheduler
):
    """Handles the /mailing command with arguments."""
    result = await _is_command_arguments_valid_(message.text.strip())

    if isinstance(result, dict):
        _subscribe_or_update_mailing_(message, scheduler, result)
        if message.chat.id not in ADMINS:
            asyncio.create_task(
                send_to_admins(
                    f"ℹ️ '{message.chat.title or message.from_user.full_name}' "
                    f"{message.chat.type} (<code>{message.chat.id}</code>) "
                    "subscribe to or update mailing."
                )
            )
        return
    await message.answer(_get_mailing_error_message_by_(result))


async def _is_command_arguments_valid_(
    command: str, check_length: Optional[bool] = True
) -> Union[ModuleType, str]:
    """Checks if the /mailing command arguments is valid
    and returns the error message key if it's not valid."""
    if check_length:
        args = command.strip().split(" ")[1:]
        if len(args) != 6:
            return "length"
    else:
        args = command.strip().split(" ")
    language, weather_provider, city, period, time_int, mute = args
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
    # Check time
    if int(time_int) not in MAILING_TIMES:
        return "time"
    # Check mute
    if mute not in ("True", "False", "t", "f", "1", "0"):
        return "mute"
    return {
        "city": result_city,
        "city_title": city.capitalize(),
        "time": time,
        "time_title": period.capitalize(),
        "lang_code": language,
        "type": "weather" if time != "review" else time,
        "mute": mute in ("True", "t", "1"),
        "time_int": int(time_int),
        "weather_provider": weather_provider,
    }


def _subscribe_or_update_mailing_(
    message: Message, scheduler: AsyncIOScheduler, data: dict
):
    """Subscribes or updates the mailing."""
    if get_mailing_by_(user_chat_id=message.chat.id) is not None:
        _remove_user_and_mailing_with_(message.chat.id, data, scheduler)
    user = _get_user_by_(message, data)
    _subscribe_mailing(user.chat_id, data, scheduler)


class MockUser(NamedTuple):
    """Represents a mock user for creating a user in the database."""

    id: int
    username: str
    full_name: str


def _get_user_by_(message: Message, data: dict) -> User:
    """Returns user or channel from the database by the given message."""
    try:
        user = get_user_by_(message.chat.id)
        assert user is not None
    except AssertionError:
        user = (
            create_user_by_(message.from_user)
            if message.chat.type == "private"
            else create_user_by_(
                MockUser(
                    id=message.chat.id,
                    username=message.chat.username,
                    full_name=message.chat.title,
                ),
                locale=data["lang_code"],
                weather_provider=data["weather_provider"],
            )
        )
    return user


def _remove_user_and_mailing_with_(
    user_chat_id: int, data: dict, scheduler: AsyncIOScheduler
):
    """Deletes the mailing for the given user chat id and subscribes the new one."""
    remove_mailing_for_(user_chat_id, scheduler)
    delete_user_with_(user_chat_id)


def _subscribe_mailing(
    user_chat_id: int, data: dict, scheduler: AsyncIOScheduler
):
    """Subscribes the mailing for the given user chat id."""
    create_mailing_for_(user_chat_id, data)
    scheduler.add_job(
        send_mailing,
        trigger="cron",
        hour=data["time_int"],
        minute=0,
        second=0,
        timezone=DEFAULT_TIMEZONE,
        id=f"mailing-{user_chat_id}",
        args=[user_chat_id],
        start_date=datetime.now(tz(DEFAULT_TIMEZONE)),
    )


def _get_mailing_error_message_by_(error: str) -> str:
    """Returns mailing error message by the given error message key."""
    return {
        **get_weather_error_messages(),
        "length": _(
            "❌ Invalid number of arguments. Expected 6 arguments: "
            "[language code: {languages}] [weather provider: {providers}] "
            "[city] [period] [time: {times}] [mute: True (t,1) / False (f,0)]) "
        ).format(
            languages=", ".join(LANGUAGES),
            providers=", ".join(WEATHER_PROVIDERS),
            times=", ".join(map(str, MAILING_TIMES)),
        ),
        "time": _("❌ Unknown time. Expected one of: {times}").format(
            times=", ".join(map(str, MAILING_TIMES))
        ),
        "mute": _("❌ Invalid mute mode. Expected: True (t,1) or False (f,0)"),
    }.get(error)

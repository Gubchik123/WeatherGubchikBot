import os
import pytz
import logging
from datetime import datetime

from aiogram.utils.exceptions import BotBlocked

from bot_info import BOT
from utils.db import UserDBInfo
from constants import MY_DB, INFO, TEXT

from .weather.parsing import (
    get_information_about_one_day,
    get_information_about_many_days,
)


cached_weather_messages = {}
logger = logging.getLogger("my_logger")


async def send_to_users() -> None:
    """For sending weather message to users with current time for mailing"""
    for user in _get_users_with_mailing_on_current_time():
        try:
            TEXT.change_on(user.lang)
            _fill_weather_information_by_(user)

            await BOT.send_message(
                user.chat_id,
                TEXT().daily_mailing_message(),
                disable_notification=user.mute,
            )
            await BOT.send_message(
                user.chat_id,
                _get_weather_info_message_by_(user.lang),
                disable_notification=user.mute,
                parse_mode="HTML",
            )
        except BotBlocked:
            logger.warning(
                f"User with chat id - {user.chat_id} has blocked the bot"
            )
            MY_DB.delete_user_with_(user.chat_id)
        except Exception as e:
            error_message = f"Exception in daily mailing (user chat id - {user.chat_id}): {str(e)}"
            logger.error(error_message)
            await BOT.send_message(
                user.chat_id,
                TEXT().error_message(),
                disable_notification=user.mute,
            )
            await _send_message_about_error_to_me(error_message)
    cached_weather_messages.clear()


def _get_users_with_mailing_on_current_time() -> tuple:
    """For getting users with current time for mailing"""
    time_zone = pytz.timezone(str(os.getenv("TIMEZONE")))
    current_hour = datetime.now(time_zone).hour

    try:
        return tuple(
            user
            for user in MY_DB.get_all_users()
            if user.time_int == current_hour
        )
    except Exception as e:
        logger.error(
            f"Exception in db during getting all users for mailing: {str(e)}"
        )
        return tuple()


def _fill_weather_information_by_(user: UserDBInfo) -> None:
    """For filling info object with user data for weather searching"""
    INFO.clean_information()

    INFO.city = user.city
    INFO.time = user.time
    INFO.type = user.type
    INFO.city_title = user.city_title


def _get_weather_info_message_by_(user_lang_code: str) -> str:
    """For getting message text with weather information"""
    user_city_and_lang_code = (INFO.city_title, user_lang_code)

    try:
        return cached_weather_messages[user_city_and_lang_code]
    except KeyError:  # If there is not such a cached message
        weather_message = (
            get_information_about_one_day()
            if INFO.about_one_day
            else get_information_about_many_days()
        )
        cached_weather_messages[user_city_and_lang_code] = weather_message
        return weather_message


async def _send_message_about_error_to_me(error_message: str) -> str:
    """For sending to me message about weather info user got"""
    await BOT.send_message(
        int(os.getenv("MY_TELEGRAM_CHAT_ID")), error_message
    )

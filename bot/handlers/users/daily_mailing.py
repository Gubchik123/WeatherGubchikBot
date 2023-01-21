import os
import pytz
import logging
from datetime import datetime

from bot_info import BOT
from utils.db import UserDBInfo
from constants import MY_DB, INFO, TEXT

from .weather.parsing import (
    get_information_about_one_day,
    get_information_about_many_days,
)


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
                _get_weather_info_message(),
                disable_notification=user.mute,
            )
        except Exception as e:
            logger.error(f"Exception in daily mailing with user: {user.chat_id}")
            logger.error(str(e))
            continue


def _get_users_with_mailing_on_current_time() -> tuple:
    """For getting users with current time for mailing"""
    time_zone = pytz.timezone(str(os.getenv("TIMEZONE")))
    current_hour = datetime.now(time_zone).hour

    try:
        return tuple(
            user for user in MY_DB.get_all_users() if user.time_int == current_hour
        )
    except Exception as e:
        logger.error(f"Exception in db: {str(e)}")
        return tuple()


def _fill_weather_information_by_(user: UserDBInfo) -> None:
    """For filling info object with user data for weather searching"""
    INFO.clean_information()

    INFO.city = user.city
    INFO.time = user.time
    INFO.type = user.type


def _get_weather_info_message() -> str:
    """For getting message text with weather information"""
    return (
        get_information_about_one_day()
        if INFO.about_one_day
        else get_information_about_many_days()
    )

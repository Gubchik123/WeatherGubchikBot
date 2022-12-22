import logging
from datetime import datetime

from bot_info import BOT
from utils.db import UserDBInfo
from constants import MY_DB, INFO, TEXT

from .weather.parsing import (
    get_information_about_one_day,
    get_information_about_many_days,
)


def get_users_with_mailing_on_current_time() -> tuple:
    """For getting users with current time for mailing"""
    datetime_now = datetime.now()

    # Hour in Ukraine UTC +2 if it's Nov, Dec, Jan, Feb, Mar else +3
    added_hour = 2 if datetime_now.month in [1, 2, 3, 11, 12] else 3
    ukrainian_hour = datetime_now.hour + added_hour

    return tuple(
        user for user in MY_DB.get_all_users() if user.time_int == ukrainian_hour
    )


def fill_weather_information_by_(user: UserDBInfo) -> None:
    """For filling info object with user data for weather searching"""
    global INFO

    INFO.clean_information()

    INFO.city = user.city
    INFO.time = user.time
    INFO.type = user.type


def get_message_text_by_(lang_code: str) -> str:
    """For getting message text with weather information"""
    global INFO, TEXT
    TEXT.change_on(lang_code)

    return (
        get_information_about_one_day()
        if INFO.about_one_day
        else get_information_about_many_days()
    )


async def send_to_users() -> None:
    """For sending weather message to users with current time for mailing"""
    for user in get_users_with_mailing_on_current_time():
        try:
            fill_weather_information_by_(user)

            await BOT.send_message(
                user.chat_id, TEXT().daily_mailing_message(),
                disable_notification=user.mute
            )
            await BOT.send_message(
                user.chat_id, get_message_text_by_(user.lang),
                disable_notification=user.mute
            )
        except:
            logger = logging.getLogger()
            logger.error(
                f"Exception in daily mailing with user: {user.chat_id}")
            continue

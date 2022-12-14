import logging
from datetime import datetime

from bot_info import BOT
from constants import MY_DB, INFO, TEXT

from .weather.parsing import (
    get_information_about_one_day,
    get_information_about_many_days,
)


def get_users_with_mailing_on_current_time() -> list[tuple]:
    """For getting users with current time for mailing"""
    datetime_now = datetime.now()
    # Hour in Ukraine UTC +2 if it's Nov, Dec, Jan, Feb, Mar else +3
    added_hour = 2 if datetime_now.month in [1, 2, 3, 11, 12] else 3
    ukrainian_hour = datetime_now.hour + added_hour

    return [
        data for data in MY_DB.get_mailing_information() if data[6] == ukrainian_hour
    ]


def fill_weather_information_by_(data: tuple) -> None:
    """For filling info object with user data for weather searching"""
    global INFO

    INFO.clean_information()

    INFO.city = data[2]
    INFO.time = data[4]
    INFO.type = data[5]


def get_message_text_by_(data: tuple) -> str:
    """For getting message text with weather information"""
    global INFO, TEXT
    TEXT.change_on(data[8])  # data[8] - language code

    return (
        get_information_about_one_day()
        if INFO.about_one_day
        else get_information_about_many_days()
    )


async def send_to_users() -> None:
    """For sending weather message to users with current time for mailing"""
    for data in get_users_with_mailing_on_current_time():
        try:
            chat_id: int = data[0]
            mute = True if data[1] else False

            fill_weather_information_by_(data)

            await BOT.send_message(
                chat_id, TEXT().daily_mailing_message(), disable_notification=mute
            )
            await BOT.send_message(
                chat_id, get_message_text_by_(data), disable_notification=mute
            )
        except:
            logger = logging.getLogger()
            logger.error(f"Exception in daily mailing with user: {chat_id}")
            continue

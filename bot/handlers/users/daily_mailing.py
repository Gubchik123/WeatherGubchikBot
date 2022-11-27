import logging
from datetime import datetime

from aiogram import Bot

from constants import MY_DB, INFO, TEXT

from .info_parsing.get_info import (
    get_information_about_one_day,
    get_information_about_many_days,
)


def get_users_with_mailing_on_current_time() -> list:
    datetime_now = datetime.now()
    added_hour = 2 if datetime_now.month in [1, 2, 3, 11, 12] else 3
    ukrainian_hour = datetime_now.hour + added_hour

    return [
        data for data in MY_DB.get_mailing_information() if data[6] == ukrainian_hour
    ]


def fill_weather_information_by_(data: tuple):
    global INFO

    INFO.clean_information()

    INFO.city = data[2]
    INFO.time = data[4]
    INFO.type = data[5]


def get_message_text_by_(data: tuple) -> str:
    global INFO, TEXT
    fill_weather_information_by_(data)
    TEXT.change_on(data[8])  # data[8] - language code

    return (
        get_information_about_one_day()
        if INFO.about_one_day
        else get_information_about_many_days()
    )


async def send_to_users(bot: Bot):
    for data in get_users_with_mailing_on_current_time():
        try:
            chat_id = data[0]
            mute = True if data[1] else False

            message_text = get_message_text_by_(data)

            await bot.send_message(
                chat_id, TEXT().daily_mailing_message(), disable_notification=mute
            )
            await bot.send_message(
                chat_id, message_text, disable_notification=mute
            )
        except:
            logger = logging.getLogger()
            logger.error(f"Exception in daily mailing with user: {chat_id}")
            continue

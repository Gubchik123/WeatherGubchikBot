import traceback
from time import sleep
from datetime import datetime

from telebot import TeleBot

from data import BOT_TOKEN
from constants import MY_DB, INFO, TEXT

from .info_parsing.general import get_soup_by_
from .info_parsing.get_info import get_information_about_one_day
from .info_parsing.get_info import get_information_about_many_days

BOT = TeleBot(BOT_TOKEN)


def get_users_with_mailing_on_current_time() -> list:
    hour_now = datetime.now().hour + 3

    return [data for data in MY_DB.get_mailing_information()
            if data[6] == hour_now]


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

    soup = get_soup_by_(INFO.generated_url)

    if INFO.about_one_day:
        return get_information_about_one_day(soup)
    elif INFO.about_many_days:
        return get_information_about_many_days(soup)


def send_to_users():
    for data in get_users_with_mailing_on_current_time():
        try:
            chat_id = data[0]
            mute = True if data[1] else False

            text = get_message_text_by_(data)

            BOT.send_message(chat_id, TEXT().daily_mailing_message(),
                             disable_notification=mute)
            BOT.send_message(chat_id, text, disable_notification=mute)
            sleep(1)
        except Exception as error:
            print(f"Exception in daily mailing with user: {chat_id}")
            print(f"In data was: {data}")
            print(f"Error message: {str(error)}")
            print(f"Traceback list: {traceback.format_exception(error)}")
            continue

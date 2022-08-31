from time import sleep
from datetime import datetime

from telebot import TeleBot

from data import BOT_TOKEN
from constants import MY_DB, INFO

from .info_parsing.general import get_soup_by
from .info_parsing.get_info import get_information_about_one_day
from .info_parsing.get_info import get_information_about_many_days

BOT = TeleBot(BOT_TOKEN)


def get_users_with_mailing_on_current_time() -> list:
    hour_now = datetime.now().hour + 3

    return [data for data in MY_DB.get_mailing_information() \
            if data[6] == hour_now]


def fill_weather_information_by_(data: tuple):
    global INFO

    INFO.clean_information()

    INFO.city = data[2]
    INFO.time = data[4]
    INFO.type = data[5]


def send_to_users():
    for data in get_users_with_mailing_on_current_time():
        try:
            chat_id = data[0]
            mute = True if data[1] else False

            fill_weather_information_by_(data)

            soup = get_soup_by(INFO.generated_url)

            if INFO.about_one_day:
                text = get_information_about_one_day(soup)
            elif INFO.about_many_days:
                text = get_information_about_many_days(soup)

            BOT.send_message(chat_id, "Щоденна розсилка",
                             disable_notification=mute)
            BOT.send_message(chat_id, text, disable_notification=mute)
            sleep(1)
        except Exception as error:
            print("Exception in daily_mailing_to_users() with user:", chat_id)
            print(str(error))
            continue

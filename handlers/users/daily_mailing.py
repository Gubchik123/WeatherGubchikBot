from time import sleep
from datetime import datetime

from telebot import TeleBot

from constants import MY_DB
from data import BOT_TOKEN
from utils.class_SelectedInfo import SelectedInfo

from .info_parsing.general import get_soup_by
from .info_parsing.get_info import get_information_about_one_day
from .info_parsing.get_info import get_and_send_information_about_many_days

BOT = TeleBot(BOT_TOKEN)


def mailing_to_users():
    hour_now = datetime.now().hour + 3

    for data in MY_DB.get_information_for_mailing():
        user_mailing_time = data[6]
        
        if user_mailing_time != hour_now:
            continue

        try:
            chat_id = data[0]
            mute = True if data[1] else False

            info = SelectedInfo()
            info.city = data[2]
            info.time = data[4]
            info.type = data[5]

            soup = get_soup_by(info.generated_url)

            if info.about_one_day:
                text = get_information_about_one_day(soup, info)
            elif info.about_many_days:
                text = get_and_send_information_about_many_days(soup)

            BOT.send_message(chat_id, "Щоденна розсилка",
                             disable_notification=mute)
            BOT.send_message(chat_id, text, disable_notification=mute)
            sleep(1)
        except Exception as error:
            print("Exception in daily_mailing_to_users() with user:", chat_id)
            print(str(error))
            continue

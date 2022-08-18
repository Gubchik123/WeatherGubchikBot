from time import sleep
from telebot import TeleBot

from constants import MY_DB
from data import BOT_TOKEN
from utils.class_SelectedInfo import SelectedInfo

from .info_parsing.general import get_soup_by
from .info_parsing.get_info import get_information_about_one_day

BOT = TeleBot(BOT_TOKEN)


def mailing_to_users():
    for data in MY_DB.get_information_for_mailing():
        try:
            chat_id = data[0]
            mute = True if data[1] else False

            info = SelectedInfo()
            info.city = data[2]

            soup = get_soup_by(info.generated_url)
            text = get_information_about_one_day(soup, info)

            BOT.send_message(chat_id, "Щоденна розсилка", disable_notification=mute)
            BOT.send_message(chat_id, text, disable_notification=mute)
            sleep(1)
        except Exception as error:
            print("Exception in daily_mailing_to_users() with user:", chat_id)
            print(str(error))
            continue

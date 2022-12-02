import traceback

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiogram import types

from constants import TEXT


def get_soup_by_(url: str):
    global TEXT

    lang_code = TEXT().lang_code

    headers = {"user-agent": UserAgent().random}
    cookie = {"cookie": f"needed_thing=''; default_lang={lang_code};"}

    if lang_code != "uk":
        url = url.replace("/ua/", f"/{lang_code}/")

    response = requests.get(url, headers=headers, cookies=cookie)
    return BeautifulSoup(response.text, "lxml")


async def send_message_to_user_about_error(message: types.Message, error):
    global TEXT
    await message.answer(TEXT().error_message())

    error_position = traceback.format_exception(error)[-2].split(r"\\")[-1]
    print("Exception place: ", error_position.replace("\n", " "))

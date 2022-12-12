import logging
import traceback

import requests
from aiogram import types
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from constants import TEXT


def get_soup_by_(url: str):
    global TEXT
    lang_code = TEXT().lang_code

    if lang_code != "uk":
        url = url.replace("/ua/", f"/{lang_code}/")

    response = requests.get(
        url,
        headers={"user-agent": UserAgent().random},
        cookies={"cookie": f"needed_thing=''; default_lang={lang_code};"},
    )
    return BeautifulSoup(response.text, "lxml")


async def send_message_to_user_about_error(message: types.Message, error):
    global TEXT
    await message.answer(TEXT().error_message())

    logger = logging.getLogger()

    error_position = traceback.format_exception(error)[-2].split(r"\\")[-1]
    error_message = "Exception place: " + error_position.replace("\n", " ")
    logger.error(error_message)

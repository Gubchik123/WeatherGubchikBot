import logging
import traceback

import requests
from aiogram import types
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from constants import TEXT


def get_soup_by_(url: str) -> BeautifulSoup:
    """For getting BeautifulSoup object by url"""
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


async def send_message_to_user_about_error(message: types.Message, error: str) -> None:
    """For sending error message to user and logging"""
    global TEXT
    await message.answer(TEXT().error_message())

    logger = logging.getLogger()
    logger.error(error)

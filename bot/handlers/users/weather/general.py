import logging

import requests
from aiogram import types
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from constants import TEXT


def get_soup_by_(url: str) -> BeautifulSoup:
    """For getting BeautifulSoup object by url"""
    lang_code = TEXT().lang_code

    if lang_code != "uk":
        url = url.replace("/ua/", f"/{lang_code}/")

    response = requests.get(
        url,
        headers={"user-agent": UserAgent().random},
        cookies={"cookie": f"needed_thing=''; default_lang={lang_code};"},
    )
    return BeautifulSoup(response.text, "lxml")


async def send_message_to_user_about_error(
    message: types.Message, error: str, message_to_user: bool = True
) -> None:
    """For sending error message to user and logging"""
    if message_to_user:
        await message.answer(TEXT().error_message())

    logger = logging.getLogger("my_logger")
    logger.error(error)

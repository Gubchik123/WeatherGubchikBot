import logging

import requests
from aiogram import types
from bs4 import BeautifulSoup
from fake_useragent import UserAgent, FakeUserAgentError

from constants import TEXT


logger = logging.getLogger("my_logger")


def _get_user_agent() -> str:
    try:
        return UserAgent().random.strip()
    except FakeUserAgentError as e:
        logger.error(f"FakeUserAgentError: {str(e)}")
        # Return default random user agent
        return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"


def get_soup_by_(url: str) -> BeautifulSoup:
    """For getting BeautifulSoup object by url"""
    lang_code = TEXT().lang_code

    if lang_code != "uk":
        url = url.replace("/ua/", f"/{lang_code}/")

    response = requests.get(
        url,
        headers={"user-agent": _get_user_agent()},
        cookies={"cookie": f"needed_thing=''; default_lang={lang_code};"},
    )
    return BeautifulSoup(response.text, "lxml")


async def send_message_to_user_about_error(
    message: types.Message, error: str, message_to_user: bool = True
) -> None:
    """For sending error message to user and logging"""
    if message_to_user:
        await message.answer(TEXT().error_message())
    logger.error(error)

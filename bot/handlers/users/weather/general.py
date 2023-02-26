import logging

import requests
from aiogram import types
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from requests.exceptions import RequestException

from constants import TEXT


logger = logging.getLogger("my_logger")


def _get_default_user_agent():
    """For getting default random User-Agent"""
    return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"


def _get_user_agent() -> str:
    """For getting random User-Agent"""
    return generate_user_agent().strip()


def _get_response_from_(url: str, lang_code: str) -> requests.Response:
    """For sending GET request to url and getting response"""
    cookies = {"cookie": f"needed_thing=''; default_lang={lang_code};"}

    try:
        return requests.get(
            url,
            cookies=cookies,
            headers={"user-agent": _get_user_agent()},
        )
    except RequestException as e:
        logger.error(f"RequestException: {str(e)}")
        return requests.get(
            url,
            cookies=cookies,
            headers={"user-agent": _get_default_user_agent()},
        )


def get_soup_by_(url: str) -> BeautifulSoup:
    """For getting BeautifulSoup object by url"""
    lang_code = TEXT().lang_code

    if lang_code != "uk":
        url = url.replace("/ua/", f"/{lang_code}/")

    return BeautifulSoup(_get_response_from_(url, lang_code).text, "lxml")


async def send_message_to_user_about_error(
    message: types.Message, error: str, message_to_user: bool = True
) -> None:
    """For sending error message to user and logging"""
    if message_to_user:
        await message.answer(TEXT().error_message())
    logger.error(error)

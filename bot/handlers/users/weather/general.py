import os
import logging

import requests
from aiogram import types
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from ..menu import menu
from bot_info import BOT
from constants import TEXT


logger = logging.getLogger("my_logger")


class InvalidResponse(Exception):
    """Exception for invalid response from GET request to the site"""


def _get_response_from_(url: str, lang_code: str) -> requests.Response:
    """For sending GET request to url and getting response"""
    response = requests.get(
        url,
        headers={"user-agent": generate_user_agent().strip()},
        cookies={"cookie": f"needed_thing=''; default_lang={lang_code};"},
    )
    if response.status_code != 200:
        raise InvalidResponse(
            f"InvalidResponse from the site ({response.status_code}); url={url}"
        )
    return response


def get_soup_by_(url: str) -> BeautifulSoup:
    """For getting BeautifulSoup object by url"""
    lang_code = TEXT().lang_code

    if lang_code != "ua":
        url = url.replace("/ua/", f"/{lang_code}/")

    return BeautifulSoup(_get_response_from_(url, lang_code).text, "lxml")


async def send_message_to_user_about_error(
    message: types.Message,
    error: str,
    error_place: str = "",
    message_to_user: bool = True,
) -> None:
    """For sending error message to user and logging"""
    if message_to_user:
        await message.answer(TEXT().try_again_message())
        await menu(message)

    logger.error(f"Exception{error_place}: {error}")
    await _send_message_about_error_to_me(message)


async def _send_message_about_error_to_me(message: types.Message) -> str:
    """For sending to me message about weather info user got"""
    my_chat_id = int(os.getenv("MY_TELEGRAM_CHAT_ID"))

    if message.from_user.id != my_chat_id:
        await BOT.send_message(my_chat_id, "There was an error")

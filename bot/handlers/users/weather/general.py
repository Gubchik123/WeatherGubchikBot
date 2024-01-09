import os
import logging

import requests
from aiogram import types
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from ..menu import menu
from bot_info import BOT
from constants import INFO, TEXT


logger = logging.getLogger("my_logger")


class InvalidResponse(Exception):
    """Exception for invalid response from GET request to the site"""


def _get_response_from_(url: str, lang_code: str) -> tuple:
    """For sending GET request to url and getting response"""
    headers = {"user-agent": generate_user_agent().strip()}
    cookies = {"cookie": f"needed_thing=''; default_lang={lang_code};"}

    response = requests.get(url, headers=headers, cookies=cookies)
    first_status_code = response.status_code

    if first_status_code in (404, 410):
        info_type = INFO.type
        info_time = INFO.time
        INFO.type = "weather"
        INFO.time = ""
        response = requests.get(
            INFO.generated_url, headers=headers, cookies=cookies
        )
        INFO.type = info_type
        INFO.time = info_time
    elif first_status_code != 200:
        raise InvalidResponse(
            f"InvalidResponse from the site ({response.status_code}); url={url}"
        )
    return (response, first_status_code)


def get_soup_by_(url: str) -> tuple:
    """For getting BeautifulSoup object by url"""
    lang_code = TEXT().lang_code

    if lang_code != "ua":
        url = url.replace("/ua/", f"/{lang_code}/")

    response, first_status_code = _get_response_from_(url, lang_code)
    return (BeautifulSoup(response.text, "lxml"), first_status_code)


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

    error_message = f"Exception{error_place}: {error}"

    logger.error(error_message)
    await _send_message_about_error_to_me(message, error_message)


async def _send_message_about_error_to_me(
    message: types.Message, error_message: str
) -> str:
    """For sending to me message about weather info user got"""
    my_chat_id = int(os.getenv("MY_TELEGRAM_CHAT_ID"))

    if message.from_user.id != my_chat_id:
        await BOT.send_message(my_chat_id, error_message)

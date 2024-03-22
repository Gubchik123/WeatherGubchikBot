import os
import logging

import requests
from bs4 import BeautifulSoup
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from user_agent import generate_user_agent

from handlers.users.menu import menu


class InvalidResponse(Exception):
    """Exception for invalid response from GET request to the site"""


def _get_response_from_(url: str, lang_code: str) -> tuple:
    """For sending GET request to url and getting response"""
    headers = {"user-agent": generate_user_agent().strip()}
    cookies = {"cookie": f"needed_thing=''; default_lang={lang_code};"}

    response = requests.get(url, headers=headers, cookies=cookies)

    if not response.ok:
        raise InvalidResponse(
            f"InvalidResponse from the site ({response.status_code}); url={url}"
        )
    return response


def get_soup_by_(url: str, lang_code: str) -> tuple:
    """For getting BeautifulSoup object by url"""
    if lang_code != "ua":
        url = url.replace("/ua/", f"/{lang_code}/")

    response = _get_response_from_(url, lang_code)
    return BeautifulSoup(response.text, "lxml")


async def send_message_to_user_about_error(
    message: Message,
    error: str,
    error_place: str = "",
    message_to_user: bool = True,
) -> None:
    """For sending error message to user and logging"""
    if message_to_user:
        await message.answer(
            _(
                "An error occurred! :(\n"
                "Please, try again or restart the bot with the /start command."
            )
        )
        await menu(message)

    error_message = f"Exception{error_place}: {error}"

    logging.error(error_message)


#     await _send_message_about_error_to_me(message, error_message)


# async def _send_message_about_error_to_me(
#     message: types.Message, error_message: str
# ) -> str:
#     """For sending to me message about weather info user got"""
#     my_chat_id = int(os.getenv("MY_TELEGRAM_CHAT_ID"))

#     if message.from_user.id != my_chat_id:
#         await BOT.send_message(my_chat_id, error_message)

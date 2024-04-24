from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from utils.weather.request import get_soup_by_
from utils.decorators import before_handler_clear_state

from ..menu import handle_menu


router = Router()


@router.message(Command("moon"))
@before_handler_clear_state
async def command_moon(message: Message, *args):
    url = "https://www.spaceweatherlive.com/uk/kalendar-misyachnih-faz.html"

    soup = get_soup_by_(url, lang_code="uk")
    moon = (
        soup.find("table", class_="table")
        .find_all("td", class_="text-center")[datetime.now().day - 1]
        .find("span")
        .text.strip()
    )
    await message.answer(_get_moon_emoji_by_(moon))
    await handle_menu(message)


def _get_moon_emoji_by_(moon: str):
    return {
        "повня": "🌕",
        "спадаючий опуклий місяць": "🌖",
        "остання чверть": "🌗",
        "спадаючий півмісяць": "🌘",
        "новий місяць": "🌑",
        "зростаючий півмісяць": "🌒",
        "перша чверть": "🌓",
        "зростаючий опуклий місяць": "🌔",
    }.get(moon.lower(), "")

from typing import Tuple

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
    """Handles the /moon command."""
    url = "https://www.moongiant.com/phase/today/"
    moon = (
        get_soup_by_(url, lang_code="uk")
        .find("div", id="todayMoonContainer")
        .find("img")
        .get("alt")
        .split(" on ")[0]
    )
    moon_phase, moon_emoji = _get_moon_phase_and_emoji_by_(moon)
    await message.answer(moon_emoji)
    await message.answer(moon_phase)
    await handle_menu(message)


def _get_moon_phase_and_emoji_by_(moon: str) -> Tuple[str, str]:
    """Returns translated moon phase and emoji by the given en moon phase."""
    return {
        "full moon": (_("Full Moon"), "🌕"),
        "waning gibbous": (_("Waning Gibbous"), "🌖"),
        "third quarter": (_("Third Quarter"), "🌗"),
        "waning crescent": (_("Waning Crescent"), "🌘"),
        "new moon": (_("New Moon"), "🌑"),
        "waxing crescent": (_("Waxing Crescent"), "🌒"),
        "first quarter": (_("First Quarter"), "🌓"),
        "waxing gibbous": (_("Waxing Gibbous"), "🌔"),
    }.get(moon.lower(), (_("Unknown"), "❔"))

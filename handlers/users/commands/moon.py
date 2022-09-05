from datetime import datetime

from aiogram import types
from googletrans import Translator

from bot_info import DP
from constants import TEXT

from ..menu import menu
from ..info_parsing.get_emoji import get_moon_emoji_by_
from ..info_parsing.general import get_soup_by, send_message_to_user_about_error


@DP.message_handler(commands="moon")
async def command_moon(message: types.Message):
    url = "https://www.spaceweatherlive.com/uk/kalendar-misyachnih-faz.html"

    try:
        day = datetime.now().day

        soup = get_soup_by(url)
        needed_punct_in_table = soup.find(
            "table",
            class_="table"
        ).find_all("td", class_="text-center")[day-1]
        moon = needed_punct_in_table.find("span").text.strip()
        moon_message = f"{moon} {get_moon_emoji_by_(moon)}"

        if TEXT.lang_code != "uk":
            moon_message = Translator().translate(moon_message, dest=TEXT.lang_code).text

        await message.answer(moon_message)
        await menu(message)
    except Exception as error:
        await send_message_to_user_about_error(message, error)

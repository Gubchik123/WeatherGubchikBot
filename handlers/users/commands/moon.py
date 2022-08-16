from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from ..menu import menu
from ..info_parsing.general import get_soup_by, print_error


@DP.message_handler(commands="moon")
@DP.message_handler(Text(equals="переглянути фазу місяця", ignore_case=True))
async def command_moon(message: types.Message):
    url = "https://www.meteoprog.ua/ua/weather/Kharkiv/"

    try:
        soup = get_soup_by(url)

        block = soup.find("div", class_="swiper-gallery")
        moon = block.find_all(
            "li", class_="overall-day-info__item")[-1].find_all("div")[1].text.strip()
        moon = moon.replace("\n", ": ")

        await message.answer(moon)
        await menu(message)
    except Exception as error:
        await print_error(message, error)

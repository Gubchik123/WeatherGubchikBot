from typing import Union

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _, lazy_gettext as __

from states.weather_search import WeatherSearch
from utils.weather.search import get_searched_data_with_

from .city_title import ask_about_city_title
from .period import ask_about_period


router = Router()


@router.message(Command(commands=("weather")))
@router.message(F.text.lower() == __("weather forecast"))
@router.callback_query(F.data == "btn_repeat_weather_city")
async def ask_about_city(
    event: Union[Message, CallbackQuery], state: FSMContext
):
    """Handles the /weather command.
    Asks user to enter the city name."""
    if isinstance(event, Message):
        message = event
    else:
        message = event.message
        await message.delete()
    # TODO: Add reply_markup with mailing city and search log cities [:4]
    await message.answer(_("Enter the name of the city / locality"))
    await state.set_state(WeatherSearch.city)


@router.message(WeatherSearch.city, F.text)
async def check_city(message: Message, i18n: I18n, state: FSMContext):
    """Requests search city and checks it."""
    user_text = message.text.lower()

    searching_message = await message.answer(_("Searching..."))

    result, is_match_100 = get_searched_data_with_(
        user_text, i18n.current_locale
    )
    if is_match_100:
        await state.update_data(
            {"city": result, "city_title": user_text.capitalize()}
        )
        await ask_about_period(message, state)
    else:
        await state.set_data({"search_cities": result})
        await ask_about_city_title(message, state)

    await searching_message.delete()

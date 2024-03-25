from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _, lazy_gettext as __

from states.weather_search import WeatherSearch
from utils.weather.search import get_searched_data_with_
from keyboards.inline.weather import get_cities_inline_keyboard
from utils.db.crud.search_log import get_last_4_search_cities_by_

from .city_title import ask_about_city_title
from .period import ask_about_period


router = Router()


@router.message(F.text.lower() == __("weather forecast"))
@router.callback_query(F.data == "btn_retry_weather_city")
async def ask_about_city(
    event: Union[Message, CallbackQuery], state: FSMContext
):
    """Asks user to enter the city name."""
    if isinstance(event, Message):
        message = event
    else:
        message = event.message
        await message.delete()
    await message.answer(
        _("Enter the name of the city / locality"),
        reply_markup=get_cities_inline_keyboard(  # TODO: Add mailing city
            cities=get_last_4_search_cities_by_(message.chat.id),
            retry_btn=False,
        ),
    )
    await state.set_state(WeatherSearch.city)


@router.message(WeatherSearch.city, F.text)
async def check_city_message(message: Message, i18n: I18n, state: FSMContext):
    """Requests search city and checks it."""
    city = message.text.lower()
    searching_message = await message.answer(_("Searching..."))

    result, is_match_100 = get_searched_data_with_(city, i18n.current_locale)

    if is_match_100:
        await state.update_data(
            {"city": result, "city_title": city.capitalize()}
        )
        await ask_about_period(message, state)
    else:
        await state.set_data({"search_cities": result})
        await ask_about_city_title(message, state)

    await searching_message.delete()


@router.callback_query(
    WeatherSearch.city, F.data.startswith("btn_city_title:")
)
async def check_city_callback_query(
    event: CallbackQuery, i18n: I18n, state: FSMContext
):
    """Requests search city and checks it."""
    city = event.data.split(":")[-1].strip().lower()

    result, _ = get_searched_data_with_(city, i18n.current_locale)

    await state.update_data({"city": result, "city_title": city.capitalize()})
    await ask_about_period(event, state)

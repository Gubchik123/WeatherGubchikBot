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
from ..other import handle_all_other_messages


router = Router()


@router.message(F.text.lower() == __("weather forecast"))
async def handle_weather(
    event: Union[Message, CallbackQuery], state: FSMContext, i18n: I18n
):
    """Starts the weather forecast search state."""
    await ask_about_city(event, i18n)
    await state.set_state(WeatherSearch.city)


@router.callback_query(F.data == "btn_retry_weather_city")
async def ask_about_city(event: Union[Message, CallbackQuery], i18n: I18n):
    """Asks user to enter the city name."""
    if isinstance(event, Message):
        message = event
        answer_method = message.answer
    else:
        message = event.message
        answer_method = message.edit_text
    await answer_method(
        _("Enter the name of the city / locality"),
        reply_markup=get_cities_inline_keyboard(  # TODO: Add mailing city
            cities=get_last_4_search_cities_by_(
                message.chat.id, i18n.current_locale
            ),
            retry_btn=False,
        ),
    )


@router.message(F.text)
async def check_city_message(message: Message, i18n: I18n, state: FSMContext):
    """Requests search city and checks it."""
    current_state = await state.get_state()
    if not current_state:
        return await handle_all_other_messages(message)

    city = message.text.lower()
    searching_message = await message.answer(_("Searching..."))

    result, is_match_100 = await get_searched_data_with_(
        city, i18n.current_locale
    )
    if is_match_100:
        await state.update_data(
            {"city": result, "city_title": city.capitalize()}
        )
        await ask_about_period(message, state)
    else:
        await state.set_data({"search_cities": result})
        await ask_about_city_title(message, state)

    await searching_message.delete()

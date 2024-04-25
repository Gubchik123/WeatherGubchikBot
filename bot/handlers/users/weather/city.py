from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _, lazy_gettext as __

from states.weather_search import WeatherSearch
from keyboards.inline.weather import get_cities_inline_keyboard
from utils.decorators import before_handler_clear_state
from utils.weather import get_weather_provider_module_by_
from utils.db.crud.user import get_user_by_
from utils.db.crud.search_log import get_last_search_cities_by_

from .city_title import ask_about_city_title
from .period import ask_about_period
from ..other import handle_all_other_messages


router = Router()


@router.message(F.text.lower() == __("weather forecast"))
@before_handler_clear_state
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
    all_user_search_logs = get_last_search_cities_by_(
        message.chat.id, i18n.current_locale
    )
    await answer_method(
        _("Enter the name of the city / locality"),
        reply_markup=get_cities_inline_keyboard(  # TODO: Add mailing city
            cities=all_user_search_logs[:4],
            all_cities_btn=len(all_user_search_logs) > 4,
            retry_btn=False,
        ),
    )


@router.callback_query(F.data == "btn_all_user_search_cities")
async def update_keyboard_with_all_user_search_cities(
    event: CallbackQuery, i18n: I18n
):
    """Updates the keyboard with all user search cities."""
    all_user_search_logs = get_last_search_cities_by_(
        event.from_user.id, i18n.current_locale
    )
    await event.message.edit_reply_markup(
        reply_markup=get_cities_inline_keyboard(
            cities=all_user_search_logs, all_cities_btn=False, retry_btn=False
        )
    )


@router.message(F.text)
async def check_city_message(message: Message, i18n: I18n, state: FSMContext):
    """Requests search city and checks it."""
    current_state = await state.get_state()
    if not current_state:
        return await handle_all_other_messages(message)

    city = message.text.lower()
    searching_message = await message.answer(_("Searching..."))

    user = get_user_by_(message.from_user.id)
    weather_provider_module = get_weather_provider_module_by_(
        user.weather_provider
    )
    result, is_match_100 = (
        await weather_provider_module.get_searched_data_with_(
            city, i18n.current_locale
        )
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

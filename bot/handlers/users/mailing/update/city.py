from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _

from states.mailing_setup import MailingSetup
from utils.db.crud.user import get_user_by_
from utils.db.crud.mailing import update_mailing_city
from utils.decorators import before_handler_clear_state
from utils.weather import get_weather_provider_module_by_
from handlers.users.weather.city import ask_about_city
from handlers.users.weather.city_title import ask_about_city_title

from ..menu import handle_mailing_menu


router = Router()


@router.callback_query(F.data == "btn_mailing_city")
@before_handler_clear_state
async def handle_mailing_city(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18n, **kwargs
):
    """Starts the mailing city state."""
    await ask_about_city(callback_query, i18n)
    await state.set_state(MailingSetup.city)


@router.message(MailingSetup.city, F.text)
async def handle_update_mailing_city(
    message: Message, state: FSMContext, i18n: I18n
):
    """Requests search city and checks it."""
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
        await state.clear()
        await _handle_update_mailing_city(
            message, city=result, city_title=city.capitalize()
        )
    else:
        await state.set_data({"search_cities": result})
        await ask_about_city_title(message, state)

    await searching_message.delete()


@router.callback_query(MailingSetup.city, F.data.startswith("btn_city_title:"))
async def handle_update_mailing_city_title(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18n
):
    """Handles updating the mailing city."""
    await state.clear()

    city = callback_query.data.split(":")[-1].strip().lower()
    city = city.split("(")[0].strip()

    user = get_user_by_(callback_query.from_user.id)
    weather_provider_module = get_weather_provider_module_by_(
        user.weather_provider
    )
    result, is_match_100 = (
        await weather_provider_module.get_searched_data_with_(
            city, i18n.current_locale
        )
    )
    update_mailing_city(
        callback_query.from_user.id, city=result, city_title=city.capitalize()
    )
    await callback_query.answer(
        _("The mailing city has been successfully updated!"),
    )
    await handle_mailing_menu(callback_query)


async def _handle_update_mailing_city(
    event: Union[Message, CallbackQuery], city: str, city_title: str
):
    """Updates the mailing city."""
    update_mailing_city(event.from_user.id, city=city, city_title=city_title)

    if isinstance(event, CallbackQuery):
        await event.answer(
            _("The mailing city has been successfully updated!"),
        )
    await handle_mailing_menu(event)

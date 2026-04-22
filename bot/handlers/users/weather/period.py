from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _

from utils.db.crud.user import get_user_by_
from states.utils import get_state_class_by_
from states.weather_search import WeatherSearch
from keyboards.inline.weather import get_period_inline_keyboard
from keyboards.inline.maker import make_yes_or_no_inline_keyboard
from filters.is_private_chat_type import IsPrivateChatType

from .send import send_weather_forecast_by_


router = Router()


@router.callback_query(F.data == "btn_mailing_period")
async def ask_about_period(
    event: Union[Message, CallbackQuery], state: FSMContext
):
    """Asks user to choose the period of the weather forecast."""
    answer_method = (
        event.answer if isinstance(event, Message) else event.message.edit_text
    )
    user = get_user_by_(event.from_user.id)
    current_state = await state.get_state()
    text = (
        _(
            "Select the forecast period or enter in how many days (2 — day after tomorrow, and so on)"
        )
        if current_state and current_state.startswith("WeatherSearch")
        else _("Select the forecast period")
    )
    await answer_method(
        text,
        reply_markup=get_period_inline_keyboard(user.weather_provider),
    )
    state_class = await get_state_class_by_(state)
    await state.set_state(state_class.period)


@router.callback_query(F.data.startswith("btn_period:"))
async def check_period(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18n
):
    """Processes the selected period of the weather forecast."""
    await callback_query.message.edit_text(_("Processing..."))
    time_title, time = callback_query.data.split(":")[1:]

    await state.update_data(
        {
            "time": time,
            "time_title": time_title,
            "lang_code": i18n.current_locale,
            "type": "weather" if time != "review" else time,
        }
    )
    current_state = await state.get_state()

    if current_state == "WeatherSearch:period":
        data = await state.get_data()
        await send_weather_forecast_by_(callback_query.message, data)

        await state.clear()
        await callback_query.message.delete()
    else:  # MailingSubscription:period
        await ask_about_mailing_mute_mode(callback_query, state)


@router.message(IsPrivateChatType(), WeatherSearch.period, F.text)
async def check_period_message(
    message: Message, state: FSMContext, i18n: I18n
):
    """Accepts a day index typed by the user."""
    data = await state.get_data()

    if not message.text.isdigit() or not (0 <= int(message.text) <= 13):
        await message.answer(_("Please enter a number from 0 to 13"))
        return

    day_index = int(message.text)

    if data.get("hourly", False) and day_index > 3:
        data["hourly"] = False

    processing_message = await message.answer(_("Processing..."))

    await state.update_data(
        {
            "day_index": day_index,
            "time": "tomorrow",
            "time_title": message.text,
            "lang_code": i18n.current_locale,
            "type": "weather",
        }
    )
    data = await state.get_data()
    await send_weather_forecast_by_(message, data)

    await state.clear()
    await processing_message.delete()


# ! Can't put it into the users/mailing/subscribe.py file because of the circular import


@router.callback_query(F.data == "btn_mailing_mute_mode")
async def ask_about_mailing_mute_mode(
    callback_query: CallbackQuery, state: FSMContext
):
    """Asks user to choose the mute mode for the mailing."""
    await callback_query.message.edit_text(
        _("Do you want to mute the mailing?"),
        reply_markup=make_yes_or_no_inline_keyboard(
            yes_callback_data="btn_mailing_mute:yes",
            no_callback_data="btn_mailing_mute:",
        ),
    )
    state_class = await get_state_class_by_(state)
    await state.set_state(state_class.mute)

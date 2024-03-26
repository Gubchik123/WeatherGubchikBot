from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _

from states.mailing_subscription import MailingSubscription
from states.utils import get_state_class_by_
from keyboards.inline.weather import get_period_inline_keyboard
from keyboards.inline.maker import make_yes_or_no_inline_keyboard

from .send import send_weather_forecast_by_


router = Router()


async def ask_about_period(
    event: Union[Message, CallbackQuery], state: FSMContext
):
    """Asks user to choose the period of the weather forecast."""
    answer_method = (
        event.answer if isinstance(event, Message) else event.message.edit_text
    )
    await answer_method(
        _("Select the forecast period"),
        reply_markup=get_period_inline_keyboard(),
    )
    state_class = await get_state_class_by_(state)
    await state.set_state(state_class.period)


@router.callback_query(F.data.startswith("btn_period:"))
async def check_period(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18n
):
    """Processes the selected period of the weather forecast."""
    await callback_query.message.edit_text(_("Processing..."))

    await state.update_data(
        {
            "time_title": callback_query.data.split(":")[-1].lower(),
            "lang_code": i18n.current_locale,
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


# ! Can't put it into the users/mailing/subscribe.py file because of the circular import
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
    await state.set_state(MailingSubscription.mute)

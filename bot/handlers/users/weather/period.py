from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _

from states.weather_search import WeatherSearch
from utils.weather.parsing import send_weather_forecast_by_
from keyboards.inline.weather import get_period_inline_keyboard


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
    await state.set_state(WeatherSearch.period)


@router.callback_query(WeatherSearch.period, F.data.startswith("btn_period:"))
async def check_period(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18n
):
    """Processes the selected period of the weather forecast."""
    wait_message = await callback_query.message.answer(_("Processing..."))
    await callback_query.message.delete()

    period = callback_query.data.split(":")[-1]

    await state.update_data(
        {"time_title": period.lower(), "lang_code": i18n.current_locale}
    )
    data = await state.get_data()

    await send_weather_forecast_by_(callback_query.message, data)

    await wait_message.delete()
    await state.clear()

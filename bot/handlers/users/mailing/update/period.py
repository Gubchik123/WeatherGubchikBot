from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from states.mailing_setup import MailingSetup
from utils.db.crud.mailing import update_mailing_period

from ..menu import handle_mailing_menu


router = Router()


@router.callback_query(MailingSetup.period, F.data.startswith("btn_period:"))
async def handle_update_mailing_period(
    callback_query: CallbackQuery, state: FSMContext
):
    """Processes the selected period of the weather forecast."""
    await state.clear()
    time_title, time = callback_query.data.split(":")[1:]

    update_mailing_period(
        callback_query.from_user.id,
        data={
            "time": time,
            "time_title": time_title,
            "type": "weather" if time != "review" else time,
        },
    )
    await callback_query.answer(
        _("The mailing period has been successfully updated!"),
    )
    await handle_mailing_menu(callback_query)

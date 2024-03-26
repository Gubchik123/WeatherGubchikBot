from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from states.mailing_setup import MailingSetup
from utils.db.crud.mailing import update_mailing_with_

from ..menu import handle_mailing_menu


router = Router()


@router.callback_query(
    MailingSetup.mute, F.data.startswith("btn_mailing_mute:")
)
async def handle_update_mailing_mute(
    callback_query: CallbackQuery, state: FSMContext
):
    """Handles updating the mailing mute mode."""
    await state.clear()
    mute = callback_query.data.endswith("yes")

    update_mailing_with_(callback_query.from_user.id, mute=mute)

    message = (
        _("The mailing has been muted!")
        if mute
        else _("The mailing has been unmuted!")
    )
    await callback_query.answer(message)
    await handle_mailing_menu(callback_query)

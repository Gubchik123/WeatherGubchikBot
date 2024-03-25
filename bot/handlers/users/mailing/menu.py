from typing import Union, Awaitable

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from utils.db.models import Mailing
from utils.db.crud.mailing import get_mailing_by_
from keyboards.inline.mailing import get_mailing_menu_inline_keyboard
from keyboards.inline.maker import make_yes_or_no_inline_keyboard


router = Router()


@router.message(F.text.lower() == __("mailing"))
@router.callback_query(F.data == "btn_mailing")
async def handle_mailing(event: Union[Message, CallbackQuery]):
    """Checks if user has mailing enabled and sends mailing menu."""
    is_callback_query = isinstance(event, CallbackQuery)
    message = event.message if is_callback_query else event
    answer_method = message.edit_text if is_callback_query else message.answer

    mailing = get_mailing_by_(user_chat_id=message.chat.id)

    if not mailing:
        return await answer_method(
            _(
                "Do you really want to set up a daily weather forecast newsletter?"
            ),
            reply_markup=make_yes_or_no_inline_keyboard(
                yes_callback_data="btn_enable_mailing",
                no_callback_data="btn_profile",
            ),
        )
    await _send_user_mailing_menu(answer_method, mailing)


async def _send_user_mailing_menu(
    answer_method: Awaitable, mailing: Mailing
) -> None:
    """Sends user mailing menu."""
    await answer_method(
        _(
            "You are in the mailing list management menu.\n"
            "Details of your newsletter:\n\n"
            "Mode: {mode}\n"
            "Daily at {time_int}:00\n\n"
            "Forecast period: {time}\n"
            "City / locality: {city}"
        ).format(
            time_int=mailing.time_int,
            mode=_("silent") if mailing.mute else _("alert"),
            time=mailing.time_title,
            city=mailing.city,
        ),
        reply_markup=get_mailing_menu_inline_keyboard(mailing.mute),
    )

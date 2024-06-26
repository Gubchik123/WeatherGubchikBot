from typing import Union, Awaitable

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from utils.db.models import Mailing
from utils.db.crud.mailing import get_mailing_by_
from keyboards.inline.mailing import get_mailing_menu_inline_keyboard
from keyboards.inline.maker import make_yes_or_no_inline_keyboard
from filters.is_private_chat_type import IsPrivateChatType


router = Router()


@router.callback_query(F.data == "btn_mailing")
@router.message(IsPrivateChatType(), F.text.lower() == __("mailing"))
async def handle_mailing_menu(event: Union[Message, CallbackQuery]):
    """Checks if user has mailing subscription and sends mailing menu."""
    is_callback_query = isinstance(event, CallbackQuery)
    message = event.message if is_callback_query else event
    answer_method = message.edit_text if is_callback_query else message.answer

    mailing = get_mailing_by_(user_chat_id=message.chat.id)

    if not mailing:
        return await answer_method(
            _(
                "Do you really want to subscribe to the daily weather forecast mailing?"
            ),
            reply_markup=make_yes_or_no_inline_keyboard(
                yes_callback_data="btn_subscribe_mailing",
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
            "<b>Mailing</b>\n\n"
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
        reply_markup=get_mailing_menu_inline_keyboard(),
    )

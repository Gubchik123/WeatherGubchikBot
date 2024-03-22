from typing import Union

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from utils.db.crud.user import get_user_by_
from utils.db.crud.mailing import get_mailing_by_
from keyboards.default.menu import get_menu_keyboard
from keyboards.inline.menu import get_menu_inline_keyboard


router = Router()


@router.message(Command(commands=["menu"]))
@router.callback_query(F.data == "btn_menu")
@router.message(F.text.lower() == __("← return to the main menu"))
async def menu(event: Union[Message, CallbackQuery]) -> None:
    """Sends the main menu to the user."""
    is_callback_query = isinstance(event, CallbackQuery)
    message = event.message if is_callback_query else event

    user = get_user_by_(user_chat_id=message.chat.id)
    if not is_callback_query:
        await message.answer(
            "---",
            reply_markup=get_menu_keyboard(
                user_mailing=get_mailing_by_(user.chat_id)
            ),
        )
    answer_method = message.edit_text if is_callback_query else message.answer
    await answer_method(
        _(
            "<b>Main menu</b>\n\n"
            "Language: <i>{locale}</i>\n"
            "Timezone: <i>{timezone}</i>\n"
            "Date you joined: <i>{created}</i>"
        ).format(
            locale=user.locale,
            timezone=user.timezone,
            created=user.created.strftime("%d.%m.%Y"),
        ),
        reply_markup=get_menu_inline_keyboard(),
    )

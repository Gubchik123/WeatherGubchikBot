from typing import Union

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery

from utils.db.crud.user import change_user_locale_by_
from keyboards.inline.language import get_language_inline_keyboard

from ..menu import menu


router = Router()


@router.message(Command(commands=["language"]))
@router.callback_query(F.data == "btn_language")
async def handle_language_command(event: Union[Message, CallbackQuery]):
    """Handles the /language command.
    Asks the user to choose a language."""
    answer_method = (
        event.message.edit_text
        if isinstance(event, CallbackQuery)
        else event.answer
    )
    await answer_method(
        "UA - Оберіть мову\nEN - Choose language\nRU - Выберите язык\n",
        reply_markup=get_language_inline_keyboard(action="menu"),
    )


@router.callback_query(F.data.startswith("btn_menu_lang"))
async def handle_choose_menu_language(callback_query: CallbackQuery):
    """Handles the language selection on menu."""
    locale = callback_query.data.split("_")[-1]
    change_user_locale_by_(callback_query.from_user.id, locale=locale)
    await callback_query.answer(
        text=_("Language successfully changed to {locale}!").format(
            locale=locale
        )
    )
    await menu(callback_query)

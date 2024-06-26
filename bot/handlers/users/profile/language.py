from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from utils.db.crud.user import update_user_with_
from keyboards.inline.profile.language import get_language_inline_keyboard

from .menu import handle_profile


router = Router()


@router.callback_query(F.data == "btn_language")
async def handle_change_language(callback_query: CallbackQuery):
    """Asks the user to choose a language."""
    await callback_query.message.edit_text(
        "UA - Оберіть мову\nEN - Choose language\nRU - Выберите язык\n",
        reply_markup=get_language_inline_keyboard(
            action="menu", back_to_profile_btn=True
        ),
    )


@router.callback_query(F.data.startswith("btn_menu_lang"))
async def handle_choose_menu_language(callback_query: CallbackQuery):
    """Handles the language selection on menu."""
    locale = callback_query.data.split("_")[-1]
    update_user_with_(callback_query.from_user.id, locale=locale)
    await callback_query.answer(
        text=_("Language successfully changed to {locale}!").format(
            locale=locale
        )
    )
    await handle_profile(callback_query)

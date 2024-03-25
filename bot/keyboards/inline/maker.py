from typing import Optional

from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_yes_or_no_inline_keyboard(
    yes_callback_data: str,
    no_callback_data: str,
    yes_btn_text: Optional[str] = None,
    no_btn_text: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Returns made inline keyboard with (yes) and (no) buttons."""
    yes_btn_text = yes_btn_text or _("Yes")
    no_btn_text = no_btn_text or _("No")

    return (
        InlineKeyboardBuilder()
        .add(
            InlineKeyboardButton(
                text=yes_btn_text, callback_data=yes_callback_data
            ),
            InlineKeyboardButton(
                text=no_btn_text, callback_data=no_callback_data
            ),
        )
        .as_markup()
    )

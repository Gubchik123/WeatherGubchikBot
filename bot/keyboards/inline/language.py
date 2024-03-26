from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .profile import get_back_to_profile_inline_button


def get_language_inline_keyboard(
    action: str, back_to_profile_btn: Optional[bool] = False
) -> InlineKeyboardMarkup:
    """Returns inline keyboard with language buttons."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="UA", callback_data=f"btn_{action}_lang_ua"),
        InlineKeyboardButton(text="EN", callback_data=f"btn_{action}_lang_en"),
        InlineKeyboardButton(text="RU", callback_data=f"btn_{action}_lang_ru"),
    )
    if back_to_profile_btn:
        keyboard.row(get_back_to_profile_inline_button())
    return keyboard.as_markup()

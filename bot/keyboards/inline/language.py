from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .profile import get_back_to_profile_inline_button


def get_language_inline_keyboard(action: str) -> InlineKeyboardMarkup:
    """Returns inline keyboard with language buttons."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="UA", callback_data=f"btn_{action}_lang_ua"
                ),
                InlineKeyboardButton(
                    text="EN", callback_data=f"btn_{action}_lang_en"
                ),
                InlineKeyboardButton(
                    text="RU", callback_data=f"btn_{action}_lang_ru"
                ),
            ],
            [get_back_to_profile_inline_button()],
        ],
    )

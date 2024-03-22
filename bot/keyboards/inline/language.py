from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
                    text="RU", callback_data=f"btn_{action}_lang_en"
                ),
            ],
        ],
    )

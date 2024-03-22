from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_menu_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns inline keyboard with the main menu inline button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Change language",
                    callback_data="btn_language",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Change timezone",
                    callback_data="btn_timezone",
                ),
            ],
        ]
    )


def get_back_to_menu_inline_button() -> InlineKeyboardButton:
    """Returns back to menu inline button."""
    return InlineKeyboardButton(
        text=_("← Return to the main menu"),
        callback_data="btn_menu",
    )

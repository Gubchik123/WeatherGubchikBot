from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_menu_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns inline keyboard with the main menu inline button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Change timezone",
                    callback_data="btn_timezone",
                ),
            ],
        ]
    )

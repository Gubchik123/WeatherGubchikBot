from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_profile_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns inline keyboard with the main menu inline button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Change language"), callback_data="btn_language"
                ),
                InlineKeyboardButton(
                    text=_("Change timezone"), callback_data="btn_timezone"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("Change weather provider"),
                    callback_data="btn_weather_provider",
                )
            ],
            [
                InlineKeyboardButton(
                    text=_("Mailing"), callback_data="btn_mailing"
                )
            ],
            [
                InlineKeyboardButton(
                    text=_("🔙 Menu"), callback_data="btn_menu"
                )
            ],
        ]
    )


def get_back_to_profile_inline_button() -> InlineKeyboardButton:
    """Returns back to menu inline button."""
    return InlineKeyboardButton(
        text=_("🔙 Profile"),
        callback_data="btn_profile",
    )

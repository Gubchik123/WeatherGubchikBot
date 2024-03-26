from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .profile import get_back_to_profile_inline_button


def get_mailing_menu_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns mailing menu inline keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Change the mute mode"),
                    callback_data="btn_mailing_mute_mode",
                ),
                InlineKeyboardButton(
                    text=_("Change the time"),
                    callback_data="btn_mailing_time_int",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("Change the forecast period"),
                    callback_data="btn_mailing_period",
                ),
                InlineKeyboardButton(
                    text=_("Change the city"), callback_data="btn_mailing_city"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("Unsubscribe"),
                    callback_data="btn_mailing_unsubscribe",
                )
            ],
            [
                get_back_to_profile_inline_button(),
            ],
        ]
    )


def get_mailing_time_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns mailing time inline keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="06:00", callback_data="btn_mailing_time_int:6"
                ),
                InlineKeyboardButton(
                    text="09:00", callback_data="btn_mailing_time_int:9"
                ),
                InlineKeyboardButton(
                    text="12:00", callback_data="btn_mailing_time_int:12"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="15:00", callback_data="btn_mailing_time_int:15"
                ),
                InlineKeyboardButton(
                    text="18:00", callback_data="btn_mailing_time_int:18"
                ),
                InlineKeyboardButton(
                    text="21:00", callback_data="btn_mailing_time_int:21"
                ),
            ],
            # [
            #     InlineKeyboardButton(
            #         text=_("Custom time"), callback_data="btn_mailing_time_int"
            #     ),
            # ],
        ]
    )

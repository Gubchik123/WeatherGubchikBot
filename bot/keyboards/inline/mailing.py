from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .profile import get_back_to_profile_inline_button


def get_mailing_menu_inline_keyboard(
    mailing_mute: bool,
) -> InlineKeyboardMarkup:
    """Returns mailing menu inline keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Unmute") if mailing_mute else _("Mute"),
                    callback_data=(
                        "btn_mailing_unmute"
                        if mailing_mute
                        else "btn_mailing_mute"
                    ),
                ),
                InlineKeyboardButton(
                    text=_("Change the time"),
                    callback_data="btn_mailing_time_int",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("Change the forecast period"),
                    callback_data="btn_mailing_time",
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

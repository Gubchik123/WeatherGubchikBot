from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton


def get_back_inline_button_by_(callback_data: str) -> InlineKeyboardButton:
    """Returns back inline button by the given callback data."""
    return InlineKeyboardButton(
        text=_("🔙 Back"),
        callback_data=callback_data,
    )

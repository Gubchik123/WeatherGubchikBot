from aiogram.utils.i18n import gettext as _
from aiogram.types import ReplyKeyboardMarkup

from .maker import make_keyboard, make_button


def get_menu_keyboard(user_mailing: bool) -> ReplyKeyboardMarkup:
    """Returns main menu keyboard."""
    return make_keyboard(
        [
            [make_button(_("Weather forecast"))],
            [
                make_button(
                    _("Mailing management")
                    if user_mailing
                    else _("Enable mailing")
                )
            ],
            [make_button(_("End communication"))],
        ]
    )

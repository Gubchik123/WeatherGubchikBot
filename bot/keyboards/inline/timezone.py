from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.countries import COUNTRIES
from .back import get_back_inline_button_by_
from .profile import get_back_to_profile_inline_button


def _get_new_callback_data(country: str = "", city: str = "") -> str:
    """Returns new timezone callback data by the given country and city."""
    return f"timezone:{country}:{city}"


def get_countries_keyboard() -> InlineKeyboardMarkup:
    """Returns inline keyboard with countries and back button."""
    keyboard = InlineKeyboardBuilder()

    for index, country in enumerate(COUNTRIES):
        keyboard_add_method = keyboard.add if index % 3 else keyboard.row
        keyboard_add_method(
            InlineKeyboardButton(
                text=country,
                callback_data=_get_new_callback_data(country),
            )
        )
    keyboard.row(get_back_to_profile_inline_button())
    return keyboard.as_markup()


def get_cities_keyboard(country: str) -> InlineKeyboardMarkup:
    """Returns inline keyboard with cities and back button."""
    keyboard = InlineKeyboardBuilder()

    for index, city in enumerate(COUNTRIES[country]):
        keyboard_add_method = keyboard.add if index % 5 else keyboard.row
        keyboard_add_method(
            InlineKeyboardButton(
                text=city,
                callback_data=_get_new_callback_data(country, city),
            )
        )
    keyboard.row(get_back_inline_button_by_("btn_timezone"))
    return keyboard.as_markup()

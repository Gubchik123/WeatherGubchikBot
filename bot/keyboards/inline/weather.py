from typing import List

from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_cities_inline_keyboard(cities: List[str]) -> InlineKeyboardMarkup:
    """Returns an inline keyboard with the given cities."""
    keyboard = InlineKeyboardBuilder()
    for index, city in enumerate(cities):
        keyboard_add_method = keyboard.add if index % 2 else keyboard.row
        keyboard_add_method(
            InlineKeyboardButton(
                text=city.capitalize(), callback_data=f"btn_city_title:{city}"
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text=_("Retry the input"), callback_data="btn_repeat_weather_city"
        )
    )
    return keyboard.as_markup()


def get_period_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns an inline keyboard with the forecast periods."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Today"), callback_data="btn_period:today"
                ),
                InlineKeyboardButton(
                    text=_("Tomorrow"), callback_data="btn_period:tomorrow"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("Week"), callback_data="btn_period:week"
                ),
                InlineKeyboardButton(
                    text=_("Fortnight"), callback_data="btn_period:fortnight"
                ),
            ],
        ]
    )

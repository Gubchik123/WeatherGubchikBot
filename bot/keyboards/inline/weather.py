from typing import List

from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.weather import get_weather_provider_module_by_


def _get_cities_inline_keyboard_builder(
    cities: List[str],
) -> InlineKeyboardBuilder:
    """Returns an inline keyboard with the given cities."""
    inline_keyboard_builder = InlineKeyboardBuilder()

    for index, city in enumerate(cities):
        keyboard_add_method = (
            inline_keyboard_builder.add
            if index % 2
            else inline_keyboard_builder.row
        )
        keyboard_add_method(
            InlineKeyboardButton(
                text=city.title(),
                callback_data=f"btn_city_title:{city}",
            )
        )
    return inline_keyboard_builder


def get_cities_inline_keyboard(
    cities: List[str],
) -> InlineKeyboardMarkup:
    """Returns an inline keyboard with all the given cities."""
    inline_keyboard_builder = _get_cities_inline_keyboard_builder(cities)
    return inline_keyboard_builder.as_markup()


def get_cities_with_expand_inline_keyboard(
    cities: List[str],
) -> InlineKeyboardMarkup:
    """Returns an inline keyboard with all the given cities."""
    inline_keyboard_builder = _get_cities_inline_keyboard_builder(cities)
    inline_keyboard_builder.row(
        InlineKeyboardButton(
            text="🔽", callback_data="btn_all_user_search_cities"
        )
    )
    return inline_keyboard_builder.as_markup()


def get_cities_with_retry_inline_keyboard(
    cities: List[str],
) -> InlineKeyboardMarkup:
    """Returns an inline keyboard with the retry button."""
    inline_keyboard_builder = _get_cities_inline_keyboard_builder(cities)
    inline_keyboard_builder.row(
        InlineKeyboardButton(
            text=_("Retry the input"),
            callback_data="btn_retry_weather_city",
        )
    )
    return inline_keyboard_builder.as_markup()


def get_period_inline_keyboard(weather_provider: str) -> InlineKeyboardMarkup:
    """Returns an inline keyboard with the forecast periods."""
    weather_provider_module = get_weather_provider_module_by_(weather_provider)

    days = {
        "now": (_("Now"), weather_provider_module.SelectedInfo.now),
        "today": (_("Today"), weather_provider_module.SelectedInfo.today),
        "tomorrow": (
            _("Tomorrow"),
            weather_provider_module.SelectedInfo.tomorrow,
        ),
        "week": (_("Week"), weather_provider_module.SelectedInfo.week),
        "fortnight": (
            _("Fortnight"),
            weather_provider_module.SelectedInfo.fortnight,
        ),
    }
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=days["now"][0],
                    callback_data=(
                        "btn_period:"
                        f"{days['now'][0].lower()}:{days['now'][1]}"
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=days["today"][0],
                    callback_data=(
                        "btn_period:"
                        f"{days['today'][0].lower()}:{days['today'][1]}"
                    ),
                ),
                InlineKeyboardButton(
                    text=days["tomorrow"][0],
                    callback_data=(
                        "btn_period:"
                        f"{days['tomorrow'][0].lower()}:{days['tomorrow'][1]}"
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=days["week"][0],
                    callback_data=(
                        "btn_period:"
                        f"{days['week'][0].lower()}:{days['week'][1]}"
                    ),
                ),
                InlineKeyboardButton(
                    text=days["fortnight"][0],
                    callback_data=(
                        "btn_period:"
                        f"{days['fortnight'][0].lower()}:{days['fortnight'][1]}"
                    ),
                ),
            ],
        ]
    )

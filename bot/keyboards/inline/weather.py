from typing import List, Optional, Union

from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.weather import get_weather_provider_module_by_


def get_cities_inline_keyboard(
    cities: List[str],
    all_cities_btn: Optional[bool] = False,
    retry_btn: Optional[bool] = True,
) -> Union[InlineKeyboardMarkup, None]:
    """Returns an inline keyboard with the given cities."""
    keyboard = InlineKeyboardBuilder()

    for index, city in enumerate(cities):
        keyboard_add_method = keyboard.add if index % 2 else keyboard.row
        keyboard_add_method(
            InlineKeyboardButton(
                text=city.title(),
                callback_data=f"btn_city_title:{city}",
            )
        )
    if all_cities_btn:
        keyboard.row(
            InlineKeyboardButton(
                text="🔽", callback_data="btn_all_user_search_cities"
            )
        )
    if retry_btn:
        keyboard.row(
            InlineKeyboardButton(
                text=_("Retry the input"),
                callback_data="btn_retry_weather_city",
            )
        )
    return keyboard.as_markup()


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

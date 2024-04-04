from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import WEATHER_PROVIDERS

from . import get_back_to_profile_inline_button


def get_weather_provider_inline_keyboard(
    except_weather_provider: Optional[str] = None,
    back_to_profile_btn: Optional[bool] = False,
) -> InlineKeyboardMarkup:
    """Returns inline keyboard with weather providers and back button."""
    keyboard = InlineKeyboardBuilder()

    for index, weather_provider in enumerate(WEATHER_PROVIDERS):
        if weather_provider == except_weather_provider:
            continue
        keyboard_add_method = keyboard.add if index % 2 else keyboard.row
        keyboard_add_method(
            InlineKeyboardButton(
                text=weather_provider,
                callback_data=f"btn_weather_provider:{weather_provider}",
            )
        )
    if back_to_profile_btn:
        keyboard.row(get_back_to_profile_inline_button())
    return keyboard.as_markup()

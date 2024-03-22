from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_keyboard(
    buttons: List[List[KeyboardButton]], one_time: bool = False
) -> ReplyKeyboardMarkup:
    """Returns aiogram reply keyboard markup."""
    return ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=one_time
    )


def make_button(title: str) -> KeyboardButton:
    """Returns aiogram keyboard button."""
    return KeyboardButton(text=title)

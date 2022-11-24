from aiogram import types


def make_keyboard(width: int, one_time: bool = False):
    return types.ReplyKeyboardMarkup(
        row_width=width, resize_keyboard=True, one_time_keyboard=one_time
    )


def make_button(title: str):
    return types.KeyboardButton(title)

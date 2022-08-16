from aiogram import types


def make_reply_keyboard_markup(width: int, one_time: bool = False):
    return types.ReplyKeyboardMarkup(row_width=width, resize_keyboard=True,
                                     one_time_keyboard=one_time)


def make_button(title: str):
    return types.KeyboardButton(title)


def make_yes_or_no_reply_keyboard_markup():
    markup = make_reply_keyboard_markup(width=2, one_time=True)
    markup.add(
        make_button("Так"),
        make_button("Ні")
    )
    return markup
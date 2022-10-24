from aiogram import types

from constants import TEXT
from .mailing_managment import managment


async def cancel_action(message: types.Message):
    global TEXT
    await message.answer(TEXT().ok_action_canceled_message())
    await managment(message)


async def there_is_no_such_type_of_answer_try_again(func, message: types.Message):
    global TEXT
    await message.answer(TEXT().there_are_not_such_type_of_answer_message())
    await func(message)


def check_language_from_(text: str):
    global TEXT
    lang_code = "uk" if "увімкнути" in text else (
        "ru" if "включить" in text else "en"
    )
    TEXT.check_language_by_(lang_code)

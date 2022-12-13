from aiogram import types

from constants import TEXT
from .menu import mailing_menu


async def cancel_action(message: types.Message):
    """For cancellation action and returning to mailing menu"""
    global TEXT
    await message.answer(TEXT().ok_action_canceled_message())
    await mailing_menu(message)


async def there_is_no_such_type_of_answer_try_again(func, message: types.Message):
    """For sending the message that there is no such answer and repeating function"""
    global TEXT
    await message.answer(TEXT().there_are_not_such_type_of_answer_message())
    await func(message)

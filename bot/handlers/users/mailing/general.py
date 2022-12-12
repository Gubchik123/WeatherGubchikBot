from aiogram import types

from constants import TEXT
from .management import management


async def cancel_action(message: types.Message):
    global TEXT
    await message.answer(TEXT().ok_action_canceled_message())
    await management(message)


async def there_is_no_such_type_of_answer_try_again(func, message: types.Message):
    global TEXT
    await message.answer(TEXT().there_are_not_such_type_of_answer_message())
    await func(message)

from aiogram import types
from aiogram.dispatcher import FSMContext

from .mailing_managment import managment


async def cancel_action(message: types.Message):
    await message.answer("Добре, дії скасовано")
    await managment(message)


async def there_is_no_such_type_of_answer_try_again(func, message: types.Message):
    await message.answer("Такої відповіді немає, перевірте та спробуйте ще раз")
    await func(message)

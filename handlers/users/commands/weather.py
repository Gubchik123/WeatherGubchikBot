from aiogram import types

from bot_info import DP
from keyboard import make_keyboard_for_country_choosing


@DP.message_handler(commands="weather")
async def command_weather(message: types.Message):
    markup = make_keyboard_for_country_choosing()
    await message.answer("Де ви бажаєте подивитися погоду?",
                         reply_markup=markup)

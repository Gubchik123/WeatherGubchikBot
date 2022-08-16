from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from bot_info import DP
from handlers.users.menu import menu


@DP.message_handler(CommandStart())
async def command_start(message: types.Message):
    sticker = "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    await message.answer_sticker(sticker)
    await message.answer(f"Привіт, {message.from_user.first_name}")
    await message.answer("Я той, хто допоможе тобі дізнатись погоду в містах України")

    await menu(message)

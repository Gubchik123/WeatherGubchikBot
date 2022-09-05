from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from bot_info import DP
from constants import TEXT
from states import Choosing

from ..menu import menu
from keyboard import make_keyboard


@DP.message_handler(CommandStart())
@DP.message_handler(commands="language")
async def choose_language(message: types.Message):
    markup = make_keyboard(width=3)
    markup.add(*("UK", "EN", "RU"))

    await message.answer("UK - Оберіть мову\n\n"
                         "EN - Choose language\n\n"
                         "RU - Выберите язык\n\n",
                         reply_markup=markup)

    await Choosing.language.set()


@DP.message_handler(state=Choosing.language)
async def check_language(message: types.Message, state: FSMContext):
    global TEXT

    user_text = message.text.lower()
    await state.finish()

    if user_text in ("uk", "en", "ru"):
        TEXT.change_on(user_text)
        await start(message)
    else:
        await choose_language(message)


async def start(message: types.Message):
    sticker = "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    await message.answer_sticker(sticker)
    await message.answer(TEXT.hello_message(message.from_user.first_name))

    await menu(message)

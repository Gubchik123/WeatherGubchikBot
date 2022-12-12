from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from bot_info import DP
from states import Choosing
from constants import TEXT, MY_DB

from ..menu import menu
from keyboard import make_keyboard


GOAL = ""


@DP.message_handler(CommandStart())
@DP.message_handler(commands="language")
async def choose_language(message: types.Message):
    global GOAL
    GOAL = "menu" if "language" in message.text else "start"

    markup = make_keyboard(width=3)
    markup.add("UK", "EN", "RU")

    await message.answer(
        "UK - Оберіть мову\nEN - Choose language\nRU - Выберите язык\n",
        reply_markup=markup,
    )
    await Choosing.language.set()


@DP.message_handler(state=Choosing.language)
async def check_language(message: types.Message, state: FSMContext):
    global TEXT, MY_DB

    user_text = message.text.lower()
    user_chat_id = message.from_user.id
    await state.finish()

    if user_text in ("uk", "en", "ru"):
        TEXT.change_on(user_text)

        if user_chat_id in MY_DB.chat_IDs:
            MY_DB.update_user_lang_with_(user_chat_id, lang=user_text)

        await start(message) if GOAL == "start" else await menu(message)
    else:
        await choose_language(message)


async def start(message: types.Message):
    await message.answer_sticker(
        "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    )
    await message.answer(TEXT().hello_message(message.from_user.first_name))
    await menu(message)

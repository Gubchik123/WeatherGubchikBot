from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from bot_info import DP
from states import Choosing
from constants import TEXT, MY_DB
from keyboard import make_keyboard

from ..menu import menu
from ..weather.general import send_message_to_user_about_error


GOAL = ""


@DP.message_handler(CommandStart())
@DP.message_handler(commands="language")
async def choose_language(message: types.Message) -> None:
    """The handler for the 'start' and 'language' command"""
    global GOAL
    GOAL = "menu" if "language" in message.text else "start"

    markup = make_keyboard(width=3)
    markup.add("UA", "EN", "RU")

    await message.answer(
        "UA - Оберіть мову\nEN - Choose language\nRU - Выберите язык\n",
        reply_markup=markup,
    )
    await Choosing.language.set()


@DP.message_handler(state=Choosing.language)
async def check_language(message: types.Message, state: FSMContext) -> None:
    """For checking language and changing if user has mailing"""
    user_text = message.text.lower()
    user_chat_id = message.from_user.id
    await state.finish()

    if user_text in ("ua", "en", "ru"):
        TEXT.change_on(user_text)

        try:
            if user_chat_id in MY_DB.chat_IDs:
                MY_DB.update_mailing_lang_code_for_user_with_(
                    chat_id=user_chat_id, new_lang_code=user_text
                )
        except Exception as e:
            await send_message_to_user_about_error(
                message,
                str(e),
                error_place=" during updating mailing lang code",
                message_to_user=False,
            )
        finally:
            await start(message) if GOAL == "start" else await menu(message)
    else:
        await choose_language(message)


async def start(message: types.Message) -> None:
    """For sending the greeting message after 'start' command"""
    await message.answer_sticker(
        "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    )
    await message.answer(TEXT().hello_message(message.from_user.first_name))
    await menu(message)

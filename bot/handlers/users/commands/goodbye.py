from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import TEXT
from keyboard import make_keyboard, make_button

from ..menu import _check_language_from_


answer_options = ("закінчити спілкування", "закончить общение", "end communication")


@DP.message_handler(commands="goodbye")
@DP.message_handler(Text(equals=answer_options[0], ignore_case=True))
@DP.message_handler(Text(equals=answer_options[1], ignore_case=True))
@DP.message_handler(Text(equals=answer_options[2], ignore_case=True))
async def command_goodbye(message: types.Message) -> None:
    """The handler for the 'goodbye' command"""
    user_text = message.text.lower()

    if user_text in answer_options:
        _check_language_from_(user_text, uk_word="спілкування", ru_word="общение")

    markup = make_keyboard(width=1)
    markup.add(make_button("/start"))

    await message.answer_sticker(
        "CAACAgIAAxkBAAICBGLIifDJ3jPz291sEcRKE5EO4j99AALsAwAC0lqIAZ0zny94Yp4oKQQ"
    )
    await message.answer(
        TEXT().goodbye_message(message.from_user.first_name), reply_markup=markup
    )

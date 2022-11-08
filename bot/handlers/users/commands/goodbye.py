from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import TEXT
from keyboard import make_keyboard, make_button

variants: tuple = (
    "закінчити спілкування",
    "закончить общение",
    "end communication"
)


@DP.message_handler(commands="goodbye")
@DP.message_handler(Text(equals=variants[0], ignore_case=True))
@DP.message_handler(Text(equals=variants[1], ignore_case=True))
@DP.message_handler(Text(equals=variants[2], ignore_case=True))
async def command_goodbye(message: types.Message):
    global TEXT
    user_text = message.text.lower()

    if user_text in variants:
        lang_code = "uk" if "спілкування" in user_text else (
            "ru" if "общение" in user_text else "en"
        )
        TEXT.check_language_by_(lang_code)

    sticker = "CAACAgIAAxkBAAICBGLIifDJ3jPz291sEcRKE5EO4j99AALsAwAC0lqIAZ0zny94Yp4oKQQ"

    markup = make_keyboard(width=1)
    markup.add(make_button("/start"))

    await message.answer_sticker(sticker)
    await message.answer(TEXT().goodbye_message(message.from_user.first_name),
                         reply_markup=markup)
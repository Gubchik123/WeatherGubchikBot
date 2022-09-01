from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from keyboard import make_keyboard, make_button


@DP.message_handler(commands="goodbye")
@DP.message_handler(Text(equals="закінчити спілкування", ignore_case=True))
async def command_goodbye(message: types.Message):
    sticker = "CAACAgIAAxkBAAICBGLIifDJ3jPz291sEcRKE5EO4j99AALsAwAC0lqIAZ0zny94Yp4oKQQ"

    markup = make_keyboard(width=1)
    markup.add(make_button("/start"))

    await message.answer_sticker(sticker)
    await message.answer(f"Бувай, {message.from_user.first_name}, повертайся ще\n"
                         "Наступного разу просто введи або натисни /start :)", reply_markup=markup)

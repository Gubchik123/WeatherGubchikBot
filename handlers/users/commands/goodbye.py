from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import TEXT
from keyboard import make_keyboard, make_button


@DP.message_handler(commands="goodbye")
@DP.message_handler(Text(equals="закінчити спілкування", ignore_case=True))
@DP.message_handler(Text(equals="закончить общение", ignore_case=True))
@DP.message_handler(Text(equals="end communication", ignore_case=True))
async def command_goodbye(message: types.Message):
    global TEXT
    sticker = "CAACAgIAAxkBAAICBGLIifDJ3jPz291sEcRKE5EO4j99AALsAwAC0lqIAZ0zny94Yp4oKQQ"

    markup = make_keyboard(width=1)
    markup.add(make_button("/start"))

    await message.answer_sticker(sticker)
    await message.answer(TEXT.goodbye_message(message.from_user.first_name),
                         reply_markup=markup)

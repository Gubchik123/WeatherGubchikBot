from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import TEXT
from states import Mailing
from keyboard import make_keyboard_for_yes_or_no_answer


@DP.message_handler(Text(equals="увімкнути розсилку", ignore_case=True))
@DP.message_handler(Text(equals="включить рассылку", ignore_case=True))
@DP.message_handler(Text(equals="enable mailing", ignore_case=True))
async def turn_on_mailing(message: types.Message):
    global TEXT
    markup = make_keyboard_for_yes_or_no_answer()

    await message.answer(
        TEXT.turn_on_mailing_question_message(),
        reply_markup=markup
    )
    await Mailing.turn_on.set()


@DP.message_handler(Text(equals="вимкнути розсилку", ignore_case=True))
@DP.message_handler(Text(equals="отключить рассылку", ignore_case=True))
@DP.message_handler(Text(equals="turn off mailing", ignore_case=True))
async def turn_off_mailing(message: types.Message):
    markup = make_keyboard_for_yes_or_no_answer()

    await message.answer(
        TEXT.turn_off_mailing_question_message(),
        reply_markup=markup
    )
    await Mailing.turn_off.set()

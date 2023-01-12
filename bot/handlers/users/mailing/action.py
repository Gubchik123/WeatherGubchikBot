from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import TEXT
from states import Mailing
from keyboard import make_keyboard_for_yes_or_no_answer

from ..menu import _check_language_from_


@DP.message_handler(Text(equals="увімкнути розсилку", ignore_case=True))
@DP.message_handler(Text(equals="включить рассылку", ignore_case=True))
@DP.message_handler(Text(equals="enable mailing", ignore_case=True))
async def turn_on_mailing(message: types.Message) -> None:
    """The handler for asking about turning on mailing"""
    _check_language_from_(message.text.lower(), uk_word="увімкнути", ru_word="включить")

    await message.answer(
        TEXT().turn_on_mailing_question_message(),
        reply_markup=make_keyboard_for_yes_or_no_answer(),
    )
    await Mailing.turn_on.set()


@DP.message_handler(Text(equals="вимкнути розсилку", ignore_case=True))
@DP.message_handler(Text(equals="отключить рассылку", ignore_case=True))
@DP.message_handler(Text(equals="turn off mailing", ignore_case=True))
async def turn_off_mailing(message: types.Message) -> None:
    """The handler for asking about turning off mailing"""
    _check_language_from_(message.text.lower(), uk_word="вимкнути", ru_word="отключить")

    await message.answer(
        TEXT().turn_off_mailing_question_message(),
        reply_markup=make_keyboard_for_yes_or_no_answer(),
    )
    await Mailing.turn_off.set()

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_info import DP
from states import Mailing
from constants import MY_DB, TEXT

from ..menu import menu
from .mailing_action import turn_off_mailing
from .general import cancel_action, there_is_no_such_type_of_answer_try_again


@DP.message_handler(state=Mailing.turn_off)
async def checking_answer_about_turning_off_mailing(message: types.Message, 
                                                    state: FSMContext):
    global TEXT
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT.yes_btn().lower():
        await withdraw_mailing_for_user(message, state)
    elif user_answer == TEXT.no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(turn_off_mailing, message)


async def withdraw_mailing_for_user(message: types.Message, state: FSMContext):
    global TEXT
    MY_DB.delete_user_with(chat_id=message.from_user.id)

    await message.answer(TEXT.successfully_turn_off_mailing_message())
    await state.finish()
    await menu(message)

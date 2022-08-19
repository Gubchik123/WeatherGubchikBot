from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_info import DP
from states import Mailing
from constants import MY_DB

from ..menu import menu
from .mailing_action import turn_off_mailing
from .general import cancel_action, there_is_no_such_type_of_answer_try_again


@DP.message_handler(state=Mailing.turn_off)
async def checking_answer_about_turning_off_mailing(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == "так":
        await withdraw_mailing_for_user(message, state)
    elif user_answer == "ні":
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(turn_off_mailing, message)


async def withdraw_mailing_for_user(message: types.Message, state: FSMContext):
    MY_DB.delete_user_with(chat_id=message.from_user.id)

    await message.answer("Ви успішно відмінили щоденну розсилку прогноза погоди")
    await state.finish()
    await menu(message)

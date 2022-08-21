from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_info import DP
from states import Mailing
from constants import MY_DB
from ..info_choosing import INFO
from utils.class_User import TelegramUser

from ..menu import menu
from ..info_choosing import choosing_region, ask_about_mailing_mute_mode
from .mailing_action import turn_on_mailing
from .general import cancel_action, there_is_no_such_type_of_answer_try_again


@DP.message_handler(state=Mailing.turn_on)
async def checking_answer_about_turning_on_mailing(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == "так":
        await state.finish()
        await choosing_region(message, goal="mailing")
    elif user_answer == "ні":
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(turn_on_mailing, message)


@DP.message_handler(state=Mailing.mute_mode)
async def checking_answer_about_mailing_mute_mode(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()

    if user_answer == "так":
        await confirm_mailing_for_user(message, mute=True, state=state)
    elif user_answer == "ні":
        await confirm_mailing_for_user(message, mute=False, state=state)
    else:
        await there_is_no_such_type_of_answer_try_again(ask_about_mailing_mute_mode, message)


async def confirm_mailing_for_user(message: types.Message, mute: bool, state):
    MY_DB.add(
        user=TelegramUser(message, mute_mode=mute),
        info=INFO
    )

    await message.answer("Ви успішно оформили розсилку")

    await state.finish()
    await menu(message)

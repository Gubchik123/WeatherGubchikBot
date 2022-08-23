from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot_info import DP
from states import Mailing
from constants import MY_DB
from keyboard import make_yes_or_no_reply_keyboard_markup

from .mailing_managment import managment
from .turning_on import select_mailing_time
from .general import cancel_action, there_is_no_such_type_of_answer_try_again


@DP.message_handler(Text("увімкнути режим оповіщення", ignore_case=True))
async def turn_off_mute_mode_for_mailing(message: types.Message):
    markup = make_yes_or_no_reply_keyboard_markup()

    await message.answer(
        "Ви дійсно хочете увімкнути режим оповіщення?",
        reply_markup=markup
    )
    await Mailing.turn_off_mute_mode.set()


@DP.message_handler(state=Mailing.turn_off_mute_mode)
async def checking_turning_on_mute_mode(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == "так":
        id = message.from_user.id
        MY_DB.update_user_with(id, what_update="mute", new_item=False)

        await managment(message)
    elif user_answer == "ні":
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(turn_off_mute_mode_for_mailing, message)


@DP.message_handler(Text("увімкнути беззвучний режим", ignore_case=True))
async def turn_on_mute_mode_for_mailing(message: types.Message):
    markup = make_yes_or_no_reply_keyboard_markup()

    await message.answer(
        "Ви дійсно хочете увімкнути беззвучний режим?",
        reply_markup=markup
    )
    await Mailing.turn_on_mute_mode.set()


@DP.message_handler(state=Mailing.turn_on_mute_mode)
async def checking_turning_on_mute_mode(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == "так":
        id = message.from_user.id
        MY_DB.update_user_with(id, what_update="mute", new_item=True)

        await managment(message)
    elif user_answer == "ні":
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(turn_on_mute_mode_for_mailing, message)


@DP.message_handler(Text("змінити час розсилки", ignore_case=True))
async def change_mailing_time(message: types.Message):
    markup = make_yes_or_no_reply_keyboard_markup()

    await message.answer(
        "Ви дійсно хочете змінити час розсилки?",
        reply_markup=markup
    )
    await Mailing.change_time.set()


@DP.message_handler(state=Mailing.change_time)
async def checking_changed_mailing_time(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == "так":
        await select_mailing_time(message, goal="changing")
    elif user_answer == "ні":
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(change_mailing_time, message)

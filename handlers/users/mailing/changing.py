from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot_info import DP
from states import Mailing
from constants import MY_DB, INFO, TEXT
from keyboard import make_keyboard_for_yes_or_no_answer
from keyboard import make_keyboard_for_country_choosing

from .mailing_managment import managment
from .turning_on import select_mailing_time
from .general import cancel_action, there_is_no_such_type_of_answer_try_again

from ..info_choosing import choose_period
from ..mailing_info import ask_about_changing_mailing_city, ask_about_changing_mailing_period


@DP.message_handler(Text("увімкнути режим оповіщення", ignore_case=True))
@DP.message_handler(Text("включить режим оповещения", ignore_case=True))
@DP.message_handler(Text("enable notification mode", ignore_case=True))
async def turn_off_mute_mode_for_mailing(message: types.Message):
    global TEXT
    TEXT.change_on_detected_language_from(message.text)

    markup = make_keyboard_for_yes_or_no_answer()

    await message.answer(
        TEXT.unmute_mailing_mode_question_message(),
        reply_markup=markup
    )
    await Mailing.turn_off_mute_mode.set()


@DP.message_handler(state=Mailing.turn_off_mute_mode)
async def checking_turning_on_mute_mode(message: types.Message, state: FSMContext):
    global TEXT
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT.yes_btn().lower():
        id = message.from_user.id
        MY_DB.update_user_with(id, what_update="mute", new_item=False)

        await managment(message)
    elif user_answer == TEXT.no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(turn_off_mute_mode_for_mailing, message)


@DP.message_handler(Text("увімкнути беззвучний режим", ignore_case=True))
@DP.message_handler(Text("включить беззвучный режим", ignore_case=True))
@DP.message_handler(Text("enable silent mode", ignore_case=True))
async def turn_on_mute_mode_for_mailing(message: types.Message):
    global TEXT
    TEXT.change_on_detected_language_from(message.text)

    markup = make_keyboard_for_yes_or_no_answer()

    await message.answer(
        TEXT.mute_mailing_mode_question_message(),
        reply_markup=markup
    )
    await Mailing.turn_on_mute_mode.set()


@DP.message_handler(state=Mailing.turn_on_mute_mode)
async def checking_turning_on_mute_mode(message: types.Message, state: FSMContext):
    global TEXT
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT.yes_btn().lower():
        id = message.from_user.id
        MY_DB.update_user_with(id, what_update="mute", new_item=True)

        await managment(message)
    elif user_answer == TEXT.no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(turn_on_mute_mode_for_mailing, message)


@DP.message_handler(Text("змінити час розсилки", ignore_case=True))
@DP.message_handler(Text("сменить время рассылки", ignore_case=True))
@DP.message_handler(Text("change the mailing time", ignore_case=True))
async def change_mailing_time(message: types.Message):
    global TEXT
    TEXT.change_on_detected_language_from(message.text)

    markup = make_keyboard_for_yes_or_no_answer()

    await message.answer(
        TEXT.change_mailing_time_question_message(),
        reply_markup=markup
    )
    await Mailing.change_time.set()


@DP.message_handler(state=Mailing.change_time)
async def checking_changed_mailing_time(message: types.Message, state: FSMContext):
    global TEXT
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT.yes_btn().lower():
        await select_mailing_time(message, goal="changing")
    elif user_answer == TEXT.no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(change_mailing_time, message)


@DP.message_handler(state=Mailing.change_city)
async def checking_changing_city(message: types.Message, state: FSMContext):
    global INFO, TEXT

    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT.yes_btn().lower():
        INFO.clean_information()
        INFO.goal = "changing mailing"

        markup = make_keyboard_for_country_choosing()
        await message.answer(TEXT.choose_mailing_country_question_message(),
                             reply_markup=markup)
    elif user_answer == TEXT.no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(ask_about_changing_mailing_city, message)


@DP.message_handler(state=Mailing.change_period)
async def checking_changing_period(message: types.Message, state: FSMContext):
    global INFO, TEXT

    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT.yes_btn().lower():
        INFO.goal = "changing mailing"
        await choose_period(message)
    elif user_answer == TEXT.no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(ask_about_changing_mailing_period, message)

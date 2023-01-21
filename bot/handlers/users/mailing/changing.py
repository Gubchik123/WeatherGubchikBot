from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot_info import DP
from states import Mailing
from constants import MY_DB, INFO, TEXT
from keyboard import make_keyboard_for_yes_or_no_answer
from keyboard import make_keyboard_for_country_choosing

from .menu import mailing_menu
from .turning_on import select_mailing_time
from .general import cancel_action, there_is_no_such_type_of_answer_try_again

from ..mailing_info import (
    ask_about_changing_mailing_city,
    ask_about_changing_mailing_period,
)
from ..menu import _check_language_from_
from ..info_choosing import choose_period
from ..weather.general import send_message_to_user_about_error


@DP.message_handler(Text("увімкнути режим оповіщення", ignore_case=True))
@DP.message_handler(Text("включить режим оповещения", ignore_case=True))
@DP.message_handler(Text("enable notification mode", ignore_case=True))
async def turn_off_mute_mode_for_mailing(message: types.Message) -> None:
    """The handler for asking about mailing alert mute mode"""
    _check_language_from_(message.text.lower(), uk_word="увімкнути", ru_word="включить")

    await message.answer(
        TEXT().unmute_mailing_mode_question_message(),
        reply_markup=make_keyboard_for_yes_or_no_answer(),
    )
    await Mailing.turn_off_mute_mode.set()


@DP.message_handler(state=Mailing.turn_off_mute_mode)
async def checking_turning_on_mute_mode(
    message: types.Message, state: FSMContext
) -> None:
    """For checking answer about turning off mailing mute mode"""
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT().yes_btn().lower():
        try:
            MY_DB.update_mailing_mute_mode_for_user_with_(
                chat_id=message.from_user.id, new_mute_mode=False
            )
        except Exception as e:
            await send_message_to_user_about_error(
                message, str(e), message_to_user=False
            )
        finally:
            await mailing_menu(message)
    elif user_answer == TEXT().no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(
            turn_off_mute_mode_for_mailing, message
        )


@DP.message_handler(Text("увімкнути беззвучний режим", ignore_case=True))
@DP.message_handler(Text("включить беззвучный режим", ignore_case=True))
@DP.message_handler(Text("enable silent mode", ignore_case=True))
async def turn_on_mute_mode_for_mailing(message: types.Message) -> None:
    """The handler for asking about mailing mute mode"""
    _check_language_from_(message.text.lower(), uk_word="увімкнути", ru_word="включить")

    await message.answer(
        TEXT().mute_mailing_mode_question_message(),
        reply_markup=make_keyboard_for_yes_or_no_answer(),
    )
    await Mailing.turn_on_mute_mode.set()


@DP.message_handler(state=Mailing.turn_on_mute_mode)
async def checking_turning_on_mute_mode(
    message: types.Message, state: FSMContext
) -> None:
    """For checking answer about turning on mailing mute mode"""
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT().yes_btn().lower():
        try:
            MY_DB.update_mailing_mute_mode_for_user_with_(
                chat_id=message.from_user.id, new_mute_mode=True
            )
        except Exception as e:
            await send_message_to_user_about_error(
                message, str(e), message_to_user=False
            )
        finally:
            await mailing_menu(message)
    elif user_answer == TEXT().no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(
            turn_on_mute_mode_for_mailing, message
        )


@DP.message_handler(Text("змінити час розсилки", ignore_case=True))
@DP.message_handler(Text("сменить время рассылки", ignore_case=True))
@DP.message_handler(Text("change the mailing time", ignore_case=True))
async def change_mailing_time(message: types.Message) -> None:
    """The handler for asking about changing mailing time"""
    _check_language_from_(message.text.lower(), uk_word="змінити", ru_word="сменить")

    await message.answer(
        TEXT().change_mailing_time_question_message(),
        reply_markup=make_keyboard_for_yes_or_no_answer(),
    )
    await Mailing.change_time.set()


@DP.message_handler(state=Mailing.change_time)
async def checking_changed_mailing_time(
    message: types.Message, state: FSMContext
) -> None:
    """For checking answer about changing mailing time"""
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT().yes_btn().lower():
        await select_mailing_time(message, goal="changing")
    elif user_answer == TEXT().no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(change_mailing_time, message)


@DP.message_handler(state=Mailing.change_city)
async def checking_changing_city(message: types.Message, state: FSMContext) -> None:
    """For checking answer about changing mailing city"""
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT().yes_btn().lower():
        INFO.clean_information()
        INFO.goal = "changing mailing"

        await message.answer(
            TEXT().choose_mailing_country_question_message(),
            reply_markup=make_keyboard_for_country_choosing(),
        )
    elif user_answer == TEXT().no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(
            ask_about_changing_mailing_city, message
        )


@DP.message_handler(state=Mailing.change_period)
async def checking_changing_period(message: types.Message, state: FSMContext) -> None:
    """For checking answer about changing mailing period"""
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT().yes_btn().lower():
        INFO.goal = "changing mailing"
        await choose_period(message)
    elif user_answer == TEXT().no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(
            ask_about_changing_mailing_period, message
        )

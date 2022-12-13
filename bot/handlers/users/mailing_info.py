from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from states import Mailing
from constants import MY_DB, INFO, TEXT
from keyboard import make_keyboard, make_button
from keyboard import make_keyboard_for_yes_or_no_answer

from .menu import _check_language_from_
from .mailing.menu import mailing_menu


@DP.message_handler(Text("змінити місто", ignore_case=True))
@DP.message_handler(Text("сменить город", ignore_case=True))
@DP.message_handler(Text("change city", ignore_case=True))
async def ask_about_changing_mailing_city(message: types.Message):
    """The handler for asking about changing mailing city"""
    global TEXT
    _check_language_from_(message.text.lower(),
                          uk_word="місто", ru_word="город")

    await message.answer(
        TEXT().change_mailing_city_question_message(),
        reply_markup=make_keyboard_for_yes_or_no_answer(),
    )
    await Mailing.change_city.set()


@DP.message_handler(Text("змінити період прогнозу", ignore_case=True))
@DP.message_handler(Text("изменить период прогноза", ignore_case=True))
@DP.message_handler(Text("change the forecast period", ignore_case=True))
async def ask_about_changing_mailing_period(message: types.Message):
    """The handler for asking about changing mailing period"""
    global TEXT
    _check_language_from_(message.text.lower(),
                          uk_word="період", ru_word="период")

    await message.answer(
        TEXT().change_mailing_period_question_message(),
        reply_markup=make_keyboard_for_yes_or_no_answer(),
    )
    await Mailing.change_period.set()


async def select_mailing_time(message: types.Message, goal: str = "mailing"):
    """For choosing mailing time"""
    global INFO
    INFO.goal = goal

    markup = make_keyboard(width=3)
    markup.add(
        *[make_button(f"{hour}:00") for hour in ("06", "09", "12", "15", "18", "21")]
    )

    await message.answer(
        TEXT().what_mailing_time_question_message(), reply_markup=markup
    )
    await Mailing.time.set()


async def ask_about_mailing_mute_mode(message: types.Message):
    """For asking about choosing mailing mute mode"""
    await message.answer(
        TEXT().mailing_mute_mode_question_message(),
        reply_markup=make_keyboard_for_yes_or_no_answer(),
    )
    await Mailing.mute_mode.set()


async def change_mailing_period(message: types.Message):
    """For changing mailing period"""
    MY_DB.update_user_with(message.from_user.id,
                           what_update="time", new_item=INFO)
    await mailing_menu(message)


async def change_mailing_city_on_(message: types.Message):
    """For changing mailing city"""
    MY_DB.update_user_with(
        message.from_user.id, what_update="city", new_item=(INFO.city, INFO.city_title)
    )
    await mailing_menu(message)

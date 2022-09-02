from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from states import Mailing
from constants import MY_DB, INFO
from keyboard import make_keyboard_for_yes_or_no_answer
from keyboard import make_keyboard, make_button

from .mailing.mailing_managment import managment


@DP.message_handler(Text("змінити місто", ignore_case=True))
async def ask_about_changing_mailing_city(message: types.Message):
    markup = make_keyboard_for_yes_or_no_answer()

    await message.answer(
        "Ви дійсно хочете змінити місто?",
        reply_markup=markup
    )
    await Mailing.change_city.set()


@DP.message_handler(Text("змінити період прогнозу", ignore_case=True))
async def ask_about_changing_mailing_period(message: types.Message):
    markup = make_keyboard_for_yes_or_no_answer()

    await message.answer(
        "Ви дійсно хочете змінити період прогнозу?",
        reply_markup=markup
    )
    await Mailing.change_period.set()


async def select_mailing_time(message: types.Message, goal: str = "mailing"):
    global INFO
    INFO.goal = goal

    markup = make_keyboard(width=3)
    markup.add(
        make_button("06:00"),
        make_button("09:00"),
        make_button("12:00"),
        make_button("15:00"),
        make_button("18:00"),
        make_button("21:00"),
    )

    await message.answer(
        "О котрій годині ви бажаєте отримувати розсилку?",
        reply_markup=markup
    )
    await Mailing.time.set()


async def ask_about_mailing_mute_mode(message: types.Message):
    markup = make_keyboard_for_yes_or_no_answer()

    await message.answer(
        "Ви бажаєте отримувати беззвучне повідомлення?",
        reply_markup=markup
    )
    await Mailing.mute_mode.set()


async def change_mailing_period(message: types.Message):
    id = message.from_user.id
    MY_DB.update_user_with(id, what_update="time", new_item=INFO)

    await managment(message)


async def change_mailing_city_on_(message: types.Message):
    id = message.from_user.id
    MY_DB.update_user_with(id, what_update="city",
                           new_item=(INFO.city, INFO.city_title))

    await managment(message)

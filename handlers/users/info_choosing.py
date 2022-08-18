from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot_info import DP
from states import Mailing
from states import Choosing
from constants import MY_DB
from utils.class_SelectedInfo import SelectedInfo
from keyboard import make_yes_or_no_reply_keyboard_markup
from keyboard import make_reply_keyboard_markup, make_button

from .mailing.mailing_managment import managment
from .info_parsing.get_info import get_info_about_weather_by_

INFO = SelectedInfo()

@DP.message_handler(Text("змінити місто", ignore_case=True))
async def change_city_for_mailing(message: types.Message):
    await choosing_region(message, goal="changing mailing")


def correct_title_from(title: str):
    if "Об" in title:
        return title.replace("Об", "об")
    elif "'Я" in title:
        return title.replace("'Я", "'я")
    else:
        return title


async def choosing_region(message: types.Message, goal: str):
    INFO.clean_information()
    INFO.goal = goal

    markup = make_reply_keyboard_markup(width=2)
    regions_list = [correct_title_from(region.title())
                    for region in INFO.region_titles]
    markup.add(*regions_list)
    await message.answer("Виберіть область", reply_markup=markup)
    await Choosing.region.set()


@DP.message_handler(state=Choosing.region)
async def checking_region(message: types.Message):
    user_text = message.text.lower()

    if user_text in INFO.region_titles:
        INFO.cities = INFO.regions[user_text]
        await choosing_city(message)
    else:
        await message.answer("Невідома область")
        await choosing_region(message, INFO.goal)


async def choosing_city(message: types.Message):
    markup = make_reply_keyboard_markup(width=3)
    cities_list = [correct_title_from(city.title())
                   for city in INFO.city_titles]
    markup.add(*cities_list)
    await message.answer("Виберіть місто", reply_markup=markup)
    await Choosing.city.set()


@DP.message_handler(state=Choosing.city)
async def checking_city(message: types.Message, state: FSMContext):
    user_text = message.text.lower()

    if user_text in INFO.city_titles:
        INFO.city = INFO.cities[user_text]

        if INFO.goal == "normal":
            await choosing_period(message)
        elif INFO.goal == "mailing":
            await state.finish()
            await ask_about_mailing_mute_mode(message)
        elif INFO.goal == "changing mailing":
            await state.finish()
            await change_(INFO.city, message)
    else:
        await message.answer("Невідоме місто")
        await choosing_city(message)


async def ask_about_mailing_mute_mode(message: types.Message):
    markup = make_yes_or_no_reply_keyboard_markup()

    await message.answer(
        "Ви бажаєте отримувати беззвучне повідомлення?",
        reply_markup=markup
    )
    await Mailing.mute_mode.set()


async def change_(city: str, message: types.Message):
    id = message.from_user.id
    MY_DB.update_user_with(id, what_update="city", new_item=city)

    await managment(message)


async def choosing_period(message: types.Message):
    markup = make_reply_keyboard_markup(width=2)
    markup.add(
        make_button("Сьогодні"),
        make_button("Завтра"),
        make_button("Тиждень"),
        make_button("Два тижня")
    )

    await message.answer("Виберіть період прогнозу", reply_markup=markup)
    await Choosing.period.set()


@DP.message_handler(state=Choosing.period)
async def checking_period(message: types.Message, state: FSMContext):
    user_text = message.text.lower()

    if user_text in ["сьогодні", "завтра", "тиждень", "два тижня"]:
        if INFO.get_time_by_(user_text) == "review":
            INFO.type = INFO.get_time_by_(user_text)
        else:
            INFO.time = INFO.get_time_by_(user_text)

        await state.finish()
        await get_info_about_weather_by_(INFO, message)
    else:
        await message.answer("Невідомий період прогнозу")
        await choosing_period(message)

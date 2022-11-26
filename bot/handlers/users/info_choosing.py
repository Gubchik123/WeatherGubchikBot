from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from fuzzywuzzy.process import extractBests

from bot_info import DP
from states import Choosing
from data.localities import *
from constants import INFO, TEXT
from keyboard import make_keyboard, make_button

from .info_parsing.get_info import get_info_about_weather_by_
from .mailing_info import (
    ask_about_mailing_mute_mode,
    change_mailing_period,
    change_mailing_city_on_,
)


async def clean_info_and_change_regions_on_(some_regions: dict, message: types.Message):
    global INFO

    goal = INFO.goal if INFO.goal else "normal"

    INFO.clean_information()
    INFO.regions = some_regions
    INFO.goal = goal

    await choose_region(message)


@DP.message_handler(Text("погода в україні", ignore_case=True))
@DP.message_handler(Text("погода в украине", ignore_case=True))
@DP.message_handler(Text("weather in ukraine", ignore_case=True))
async def weather_in_Ukraine(message: types.Message):
    global TEXT
    lang_code = (
        "uk"
        if "україні" in message.text.lower()
        else ("ru" if "украине" in message.text.lower() else "en")
    )
    TEXT.check_language_by_(lang_code)

    ukr_regions = {"uk": UK_UKR_LOCALITIES, "ru": RU_UKR_LOCALITIES}.get(
        TEXT().lang_code, EN_UKR_LOCALITIES
    )

    await clean_info_and_change_regions_on_(ukr_regions, message)


@DP.message_handler(Text("погода в європі", ignore_case=True))
@DP.message_handler(Text("погода в европе", ignore_case=True))
@DP.message_handler(Text("weather in europe", ignore_case=True))
async def weather_in_Europe(message: types.Message):
    global TEXT
    lang_code = (
        "uk"
        if "європі" in message.text.lower()
        else ("ru" if "европе" in message.text.lower() else "en")
    )
    TEXT.check_language_by_(lang_code)

    abroad_regions = {"uk": UK_ABROAD_LOCALITIES, "ru": RU_ABROAD_LOCALITIES}.get(
        TEXT().lang_code, EN_ABROAD_LOCALITIES
    )

    await clean_info_and_change_regions_on_(abroad_regions, message)


async def choose_region(message: types.Message):
    global TEXT
    await message.answer(
        TEXT().choose_region_message(), reply_markup=types.ReplyKeyboardRemove()
    )
    await Choosing.region.set()


async def check_user_goal_on_region_phase(message: types.Message, state: FSMContext):
    if INFO.goal in ("normal", "mailing"):
        await choose_period(message)
    elif INFO.goal == "changing mailing":
        await state.finish()
        await change_mailing_city_on_(message)


@DP.message_handler(state=Choosing.region)
async def check_selected_region(message: types.Message, state: FSMContext):
    user_text = message.text.lower()

    await message.answer(TEXT().wait_message())

    result: list = extractBests(user_text, INFO.region_titles, limit=4)

    if result[0][1] == 100:
        INFO.city = INFO.regions[user_text]
        INFO.city_title = user_text.capitalize()

        await check_user_goal_on_region_phase(message, state)
    else:
        await state.set_data({"result_list": [data[0] for data in result]})

        await choose_region_title(message, state)


async def choose_region_title(message: types.Message, state: FSMContext):
    global TEXT
    result_list = await state.get_data("result_list")

    markup = make_keyboard(width=2)
    markup.add(*[title.capitalize() for title in result_list["result_list"]])
    markup.add(make_button(TEXT().repeat_choosing_btn()))

    await message.answer(TEXT().choose_minded_option(), reply_markup=markup)

    await Choosing.region_title.set()


@DP.message_handler(state=Choosing.region_title)
async def check_selected_region_title(message: types.Message, state: FSMContext):
    global TEXT
    user_text = message.text.lower()
    result = await state.get_data("result_list")

    if user_text in result["result_list"]:
        INFO.city = INFO.regions[user_text]
        INFO.city_title = user_text.capitalize()

        await check_user_goal_on_region_phase(message, state)
    elif user_text == TEXT().repeat_choosing_btn().lower():
        await choose_region(message)
    else:
        await message.answer(TEXT().there_are_not_such_type_of_region_message())
        await choose_region_title(message, state)


async def choose_period(message: types.Message):
    global TEXT
    periods: tuple = (
        TEXT().today_btn(),
        TEXT().tomorrow_btn(),
        TEXT().week_btn(),
        TEXT().two_week_btn(),
    )

    markup = make_keyboard(width=2)
    markup.add(*periods)

    await message.answer(TEXT().choose_period_message(), reply_markup=markup)
    await Choosing.period.set()


def check_selected_period_it_is_week_or_other():
    if INFO.get_time() == "review":
        INFO.type = INFO.get_time()
    else:
        INFO.time = INFO.get_time()


async def check_user_goal_on_period_phase(message: types.Message):
    await message.answer(TEXT().wait_message())

    if INFO.goal == "normal":
        await get_info_about_weather_by_(message)
    elif INFO.goal == "mailing":
        await ask_about_mailing_mute_mode(message)
    elif INFO.goal == "changing mailing":
        await change_mailing_period(message)


@DP.message_handler(state=Choosing.period)
async def check_selected_period(message: types.Message, state: FSMContext):
    global TEXT
    periods: tuple = (
        TEXT().today_btn(),
        TEXT().tomorrow_btn(),
        TEXT().week_btn(),
        TEXT().two_week_btn(),
    )

    user_text = message.text.lower()

    if user_text in [period.lower() for period in periods]:
        INFO.time_title = user_text

        check_selected_period_it_is_week_or_other()

        await state.finish()
        await check_user_goal_on_period_phase(message)
    else:
        await message.answer(TEXT().there_are_not_such_type_of_period_message())
        await choose_period(message)

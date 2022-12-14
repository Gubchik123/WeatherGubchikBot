from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from fuzzywuzzy.process import extractBests

from bot_info import DP
from states import Choosing
from data.localities import *
from constants import INFO, TEXT
from keyboard import make_keyboard, make_button

from .mailing_info import (
    ask_about_mailing_mute_mode,
    change_mailing_period,
    change_mailing_city_on_,
)
from .menu import _check_language_from_
from .weather.parsing import get_info_about_weather_by_


async def _clean_info_and_change_regions_on_(
    some_regions: dict, message: types.Message
) -> None:
    """For cleaning weather info and changing region for weather searching"""
    global INFO

    goal = INFO.goal if INFO.goal else "normal"

    INFO.clean_information()
    INFO.regions = some_regions
    INFO.goal = goal

    await choose_region(message)


@DP.message_handler(Text("погода в україні", ignore_case=True))
@DP.message_handler(Text("погода в украине", ignore_case=True))
@DP.message_handler(Text("weather in ukraine", ignore_case=True))
async def weather_in_Ukraine(message: types.Message) -> None:
    """The handler for getting weather information in Ukraine"""
    global TEXT
    _check_language_from_(message.text.lower(), uk_word="україні", ru_word="украине")

    ukr_regions = {"uk": UK_UKR_LOCALITIES, "ru": RU_UKR_LOCALITIES}.get(
        TEXT().lang_code, EN_UKR_LOCALITIES
    )

    await _clean_info_and_change_regions_on_(ukr_regions, message)


@DP.message_handler(Text("погода в європі", ignore_case=True))
@DP.message_handler(Text("погода в европе", ignore_case=True))
@DP.message_handler(Text("weather in europe", ignore_case=True))
async def weather_in_Europe(message: types.Message) -> None:
    """The handler for getting weather information in Europe"""
    global TEXT
    _check_language_from_(message.text.lower(), uk_word="європі", ru_word="европе")

    abroad_regions = {"uk": UK_ABROAD_LOCALITIES, "ru": RU_ABROAD_LOCALITIES}.get(
        TEXT().lang_code, EN_ABROAD_LOCALITIES
    )

    await _clean_info_and_change_regions_on_(abroad_regions, message)


async def choose_region(message: types.Message) -> None:
    """For choosing weather region"""
    global TEXT
    await message.answer(
        TEXT().choose_region_message(), reply_markup=types.ReplyKeyboardRemove()
    )
    await Choosing.region.set()


def _check_the_match_is_100_between_user_option_and_(result: str) -> bool:
    """For checking the match is 100% between user option and extracted option"""
    return result[0][1] == 100


async def check_user_goal_on_region_phase(
    message: types.Message, state: FSMContext
) -> None:
    """For checking user goal for further actions"""
    if INFO.goal in ("normal", "mailing"):
        await choose_period(message)
    elif INFO.goal == "changing mailing":
        await state.finish()
        await change_mailing_city_on_(message)


@DP.message_handler(state=Choosing.region)
async def check_selected_region(message: types.Message, state: FSMContext) -> None:
    """For checking selected weather region"""
    user_text = message.text.lower()

    await message.answer(TEXT().searching_message())

    result: list = extractBests(user_text, INFO.region_titles, limit=4)

    if _check_the_match_is_100_between_user_option_and_(result):
        INFO.city = INFO.regions[user_text]
        INFO.city_title = user_text.capitalize()

        await check_user_goal_on_region_phase(message, state)
    else:
        await state.set_data({"result_list": [data[0] for data in result]})
        await choose_region_title(message, state)


async def choose_region_title(message: types.Message, state: FSMContext) -> None:
    """For choosing weather region the user had in mind"""
    global TEXT
    result: list[str] = await state.get_data("result_list")

    markup = make_keyboard(width=2)
    markup.add(*[title.capitalize() for title in result["result_list"]])
    markup.add(make_button(TEXT().repeat_choosing_btn()))

    await message.answer(TEXT().choose_minded_option(), reply_markup=markup)
    await Choosing.region_title.set()


@DP.message_handler(state=Choosing.region_title)
async def check_selected_region_title(
    message: types.Message, state: FSMContext
) -> None:
    """For checking weather region the user had in mind"""
    global TEXT
    user_text = message.text.lower()
    result: list[str] = await state.get_data("result_list")

    if user_text in result["result_list"]:
        INFO.city = INFO.regions[user_text]
        INFO.city_title = user_text.capitalize()

        await check_user_goal_on_region_phase(message, state)
    elif user_text == TEXT().repeat_choosing_btn().lower():
        await choose_region(message)
    else:
        await message.answer(TEXT().there_are_not_such_type_of_region_message())
        await choose_region_title(message, state)


def _get_weather_period_buttons() -> tuple[str]:
    """For getting buttons with weather periods"""
    return (
        TEXT().today_btn(),
        TEXT().tomorrow_btn(),
        TEXT().week_btn(),
        TEXT().two_week_btn(),
    )


async def choose_period(message: types.Message) -> None:
    """For choosing weather period"""
    global TEXT

    markup = make_keyboard(width=2)
    markup.add(*_get_weather_period_buttons())

    await message.answer(TEXT().choose_period_message(), reply_markup=markup)
    await Choosing.period.set()


def check_selected_period_it_is_week_or_other() -> None:
    """For checking and setting weather period"""
    if INFO.get_time() == "review":
        INFO.type = INFO.get_time()
    else:
        INFO.time = INFO.get_time()


async def check_user_goal_on_period_phase(message: types.Message) -> None:
    """For checking user goal for further actions"""
    await message.answer(TEXT().wait_message())

    if INFO.goal == "normal":
        await get_info_about_weather_by_(message)
    elif INFO.goal == "mailing":
        await ask_about_mailing_mute_mode(message)
    elif INFO.goal == "changing mailing":
        await change_mailing_period(message)


@DP.message_handler(state=Choosing.period)
async def check_selected_period(message: types.Message, state: FSMContext) -> None:
    """For checking selected weather period"""
    global TEXT
    user_text = message.text.lower()

    if user_text in [period.lower() for period in _get_weather_period_buttons()]:
        INFO.time_title = user_text

        check_selected_period_it_is_week_or_other()

        await state.finish()
        await check_user_goal_on_period_phase(message)
    else:
        await message.answer(TEXT().there_are_not_such_type_of_period_message())
        await choose_period(message)

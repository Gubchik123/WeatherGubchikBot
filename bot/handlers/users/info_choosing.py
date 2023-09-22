import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot_info import DP
from states import Choosing
from constants import INFO, TEXT, MY_DB
from keyboard import make_keyboard, make_button

from .mailing_info import (
    ask_about_mailing_mute_mode,
    change_mailing_period,
    change_mailing_city_on_,
)
from .menu import _check_language_from_
from .weather.search import get_searched_data_with_
from .weather.parsing import get_info_about_weather_by_
from .weather.general import send_message_to_user_about_error


logger = logging.getLogger("my_logger")
where_weather = "foreign"
mailing_city = last_city = ""


async def _clean_info_and_continue(message: types.Message) -> None:
    """For cleaning weather info and changing region for weather searching"""
    goal = INFO.goal if INFO.goal else "normal"

    INFO.clean_information()
    INFO.goal = goal

    await choose_region(message)


@DP.message_handler(Text("прогноз погоди", ignore_case=True))
@DP.message_handler(Text("прогноз погоды", ignore_case=True))
@DP.message_handler(Text("weather forecast", ignore_case=True))
async def weather_forecast(message: types.Message) -> None:
    """The handler for getting weather information"""
    _check_language_from_(
        message.text.lower(), uk_word="погоди", ru_word="погоды"
    )
    await _clean_info_and_continue(message)


async def _set_mailing_city_and_last_city(message: types.Message):
    global mailing_city, last_city

    try:
        mailing_city, last_city = MY_DB.get_columns_for_user_with_(
            message.from_user.id,
            columns=f"city_title, last_{where_weather}_city",
        )
    except Exception as e:
        await send_message_to_user_about_error(
            message,
            str(e),
            error_place=" during getting last_city",
            message_to_user=False,
        )


async def _get_choosing_region_markup_by_(
    message: types.Message,
) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardRemove()  # Default keyboard

    if message.from_user.id in MY_DB.chat_IDs:
        await _set_mailing_city_and_last_city(message)
        markup = make_keyboard(width=2)
        markup.add(
            *(mailing_city, last_city)
            if last_city and mailing_city != last_city
            else (mailing_city,)
        )
    return markup


async def choose_region(message: types.Message) -> None:
    """For choosing weather region"""
    await message.answer(
        TEXT().choose_region_message(),
        reply_markup=await _get_choosing_region_markup_by_(message),
    )
    await Choosing.region.set()


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
async def check_selected_region(
    message: types.Message, state: FSMContext
) -> None:
    """For checking selected weather region"""
    user_text = message.text.lower()

    await message.answer(TEXT().searching_message())

    result, is_match_100 = get_searched_data_with_(user_text)

    if is_match_100:
        INFO.city = result
        INFO.city_title = user_text.capitalize()

        await check_user_goal_on_region_phase(message, state)
    else:
        await state.set_data({"result_list": result})
        await choose_region_title(message, state)


async def choose_region_title(
    message: types.Message, state: FSMContext
) -> None:
    """For choosing weather region the user had in mind"""
    result: dict = await state.get_data("result_list")

    markup = make_keyboard(width=2)
    markup.add(
        *[city_title.title() for city_title in result["result_list"]]
    )
    markup.add(make_button(TEXT().repeat_choosing_btn()))

    await message.answer(TEXT().choose_minded_option(), reply_markup=markup)
    await Choosing.region_title.set()


@DP.message_handler(state=Choosing.region_title)
async def check_selected_region_title(
    message: types.Message, state: FSMContext
) -> None:
    """For checking weather region the user had in mind"""
    user_text = message.text.lower()
    result: dict = await state.get_data("result_list")

    if user_text in result["result_list"].keys():
        INFO.city = result["result_list"][user_text]
        INFO.city_title = user_text.title()

        await check_user_goal_on_region_phase(message, state)
    elif user_text == TEXT().repeat_choosing_btn().lower():
        await choose_region(message)
    else:
        await message.answer(
            TEXT().there_are_not_such_type_of_region_message()
        )
        await choose_region_title(message, state)


async def _update_user_last_searched_city_by_(message: types.Message) -> None:
    """For updating the user's last searched city if the user exists in db"""
    chat_id, user_text = message.from_user.id, message.text.capitalize()

    try:
        if chat_id in MY_DB.chat_IDs and user_text not in (
            mailing_city,
            last_city,
        ):
            MY_DB.update_last_city_for_user_with_(
                chat_id, city_type=where_weather, new_last_city=user_text
            )
    except Exception as e:
        await send_message_to_user_about_error(
            message,
            str(e),
            error_place=" during updating last_city",
            message_to_user=False,
        )


def _get_weather_period_buttons() -> tuple:
    """For getting buttons with weather periods"""
    return (
        TEXT().today_btn(),
        TEXT().tomorrow_btn(),
        TEXT().week_btn(),
        TEXT().two_week_btn(),
    )


async def choose_period(message: types.Message) -> None:
    """For choosing weather period"""
    if INFO.goal == "normal":
        await _update_user_last_searched_city_by_(message)

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
async def check_selected_period(
    message: types.Message, state: FSMContext
) -> None:
    """For checking selected weather period"""
    user_text = message.text.lower()

    if user_text in [
        period.lower() for period in _get_weather_period_buttons()
    ]:
        INFO.time_title = user_text

        check_selected_period_it_is_week_or_other()

        await state.finish()
        await check_user_goal_on_period_phase(message)
    else:
        await message.answer(
            TEXT().there_are_not_such_type_of_period_message()
        )
        await choose_period(message)

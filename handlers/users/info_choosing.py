from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from fuzzywuzzy.process import extractBests

from bot_info import DP
from constants import INFO
from states import Choosing
from keyboard import make_keyboard, make_button

from .info_parsing.get_info import get_info_about_weather_by_
from .mailing_info import ask_about_mailing_mute_mode, change_mailing_period, change_mailing_city_on_


async def change_regions_dict_on_(some_regions: dict, message: types.Message):
    global INFO

    goal = INFO.goal

    INFO.clean_information()
    INFO.regions = some_regions
    INFO.goal = goal

    await choose_region(message)


@DP.message_handler(Text("погода в україні", ignore_case=True))
async def weather_in_Ukraine(message: types.Message):
    await change_regions_dict_on_(INFO.ukr_regions, message)


@DP.message_handler(Text("погода в європі", ignore_case=True))
async def weather_in_Europe(message: types.Message):
    await change_regions_dict_on_(INFO.abroad_regions, message)


async def choose_region(message: types.Message):
    await message.answer(
        "Введіть назву міста / населеного пункту\n"
        "(Раджу використовувати українську мову)",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await Choosing.region.set()


async def check_user_goal_on_region_phase(message, state):
    if INFO.goal in ("normal", "mailing"):
        await choose_period(message)
    elif INFO.goal == "changing mailing":
        await state.finish()
        await change_mailing_city_on_(INFO.city, message)


@DP.message_handler(state=Choosing.region)
async def check_selected_region(message: types.Message, state: FSMContext):
    user_text = message.text.lower()

    result: list = extractBests(user_text, INFO.region_titles, limit=4)

    if result[0][1] == 100:
        INFO.city = INFO.regions[user_text]

        await check_user_goal_on_region_phase(message, state)
    else:
        await state.set_data({"result_list": [data[0] for data in result]})

        await choose_region_title(message, state)


async def choose_region_title(message: types.Message, state: FSMContext):
    result_list = await state.get_data("result_list")

    markup = make_keyboard(width=2)
    markup.add(*[title.capitalize() for title in result_list["result_list"]])
    markup.add(make_button("Повторити спробу введення"))

    await message.answer(
        "Оберіть варіант, який ви мали на увазі",
        reply_markup=markup
    )

    await Choosing.region_title.set()


@DP.message_handler(state=Choosing.region_title)
async def check_selected_region_title(message: types.Message,
                                      state: FSMContext):
    user_text = message.text.lower()
    result = await state.get_data("result_list")

    if user_text in result["result_list"]:
        INFO.city = INFO.regions[user_text]

        await check_user_goal_on_region_phase(message, state)
    elif user_text == "повторити спробу введення":
        await choose_region(message)
    else:
        await message.answer("Ви обрали не той варіант")
        await choose_region_title(message, state)


async def choose_period(message: types.Message):
    markup = make_keyboard(width=2)
    markup.add(*["Сьогодні", "Завтра", "Тиждень", "Два тижня"])

    await message.answer("Виберіть період прогнозу", reply_markup=markup)
    await Choosing.period.set()


def check_selected_period_it_is_week_or_other():
    if INFO.get_time() == "review":
        INFO.type = INFO.get_time()
    else:
        INFO.time = INFO.get_time()


async def check_user_goal_on_period_phase(message: types.Message):
    if INFO.goal == "normal":
        await get_info_about_weather_by_(message)
    elif INFO.goal == "mailing":
        await ask_about_mailing_mute_mode(message)
    elif INFO.goal == "changing mailing":
        await change_mailing_period(message)


@DP.message_handler(state=Choosing.period)
async def check_selected_period(message: types.Message, state: FSMContext):
    user_text = message.text.lower()

    if user_text in ["сьогодні", "завтра", "тиждень", "два тижня"]:
        INFO.time_title = user_text

        check_selected_period_it_is_week_or_other()

        await state.finish()
        await check_user_goal_on_period_phase(message)
    else:
        await message.answer("Невідомий період прогнозу")
        await choose_period(message)

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from fuzzywuzzy.process import extractBests

from bot_info import DP
from constants import MY_DB
from states import Mailing, Choosing
from utils.class_SelectedInfo import SelectedInfo
from keyboard import make_yes_or_no_reply_keyboard_markup
from keyboard import make_reply_keyboard_markup, make_button

from .mailing.mailing_managment import managment
from .info_parsing.get_info import get_info_about_weather_by_
from .mailing.general import cancel_action, there_is_no_such_type_of_answer_try_again


INFO = SelectedInfo()


@DP.message_handler(Text("змінити місто", ignore_case=True))
async def change_city_for_mailing(message: types.Message):
    markup = make_yes_or_no_reply_keyboard_markup()

    await message.answer(
        "Ви дійсно хочете змінити місто?",
        reply_markup=markup
    )
    await Mailing.change_city.set()


@DP.message_handler(state=Mailing.change_city)
async def checking_changing_city(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == "так":
        await choosing_region(message, goal="changing mailing")
    elif user_answer == "ні":
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(change_city_for_mailing, message)


@DP.message_handler(Text("змінити період прогнозу", ignore_case=True))
async def change_period_for_mailing(message: types.Message):
    markup = make_yes_or_no_reply_keyboard_markup()

    await message.answer(
        "Ви дійсно хочете змінити період прогнозу?",
        reply_markup=markup
    )
    await Mailing.change_period.set()


@DP.message_handler(state=Mailing.change_period)
async def checking_changing_periody(message: types.Message, state: FSMContext):
    global INFO

    user_answer = message.text.lower()
    await state.finish()

    if user_answer == "так":
        INFO.goal = "changing mailing"
        await choosing_period(message)
    elif user_answer == "ні":
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(change_period_for_mailing, message)


async def select_mailing_time(message: types.Message, goal: str = "adding"):
    global INFO
    INFO.goal = goal

    markup = make_reply_keyboard_markup(width=3)

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


async def choosing_region(message: types.Message, goal: str):
    INFO.clean_information()
    INFO.goal = goal

    await message.answer(
        "Введіть назву міста / населеного пункту\n(Раджу використовувати українську мову)",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await Choosing.region.set()


@DP.message_handler(state=Choosing.region)
async def checking_region(message: types.Message, state: FSMContext):
    await message.answer("Процес пошуку...")

    result: list = extractBests(
        message.text.lower(), INFO.region_titles, limit=4)
    await state.set_data({"result_list": [data[0] for data in result]})

    await choosing_region_title(
        message,
        result_list=[data[0].capitalize() for data in result]
    )


async def choosing_region_title(message: types.Message, result_list: list):
    markup = make_reply_keyboard_markup(width=2)
    markup.add(*result_list)

    await message.answer(
        "Оберіть варіант, який ви мали на увазі",
        reply_markup=markup
    )
    await Choosing.region_title.set()


@DP.message_handler(state=Choosing.region_title)
async def checking_region_title(message: types.Message, state: FSMContext):
    user_text = message.text.lower()
    result = await state.get_data("result_list")

    if user_text in result["result_list"]:

        if INFO.goal == "normal":
            INFO.city = INFO.regions[user_text]
            await choosing_period(message)
        elif INFO.goal == "mailing":
            await ask_about_mailing_mute_mode(message)
        elif INFO.goal == "changing mailing":
            await change_mailing_period_by_(message)
            
    else:
        await message.answer("Ви обрали не той варіант")
        await choosing_region_title(
            message, 
            result_list=[data.capitalize() for data in result["result_list"]]
        )


async def ask_about_mailing_mute_mode(message: types.Message):
    markup = make_yes_or_no_reply_keyboard_markup()

    await message.answer(
        "Ви бажаєте отримувати беззвучне повідомлення?",
        reply_markup=markup
    )
    await Mailing.mute_mode.set()


async def change_mailing_city_by_(city: str, message: types.Message):
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
        INFO.time_title = user_text

        if INFO.get_time() == "review":
            INFO.type = INFO.get_time()
        else:
            INFO.time = INFO.get_time()

        await state.finish()

        if INFO.goal == "normal":
            await get_info_about_weather_by_(INFO, message)
        elif INFO.goal == "mailing":
            await ask_about_mailing_mute_mode(message)
        elif INFO.goal == "changing mailing":
            await change_mailing_period_by_(message)
    else:
        await message.answer("Невідомий період прогнозу")
        await choosing_period(message)


async def change_mailing_period_by_(message: types.Message):
    id = message.from_user.id
    MY_DB.update_user_with(id, what_update="time", new_item=INFO)

    await managment(message)

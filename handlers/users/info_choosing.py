from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

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

    markup = make_reply_keyboard_markup(width=2)
    regions_list = [region.capitalize() for region in INFO.region_titles]
    markup.add(*regions_list)
    await message.answer("Виберіть область", reply_markup=markup)
    await Choosing.region.set()


@DP.message_handler(state=Choosing.region)
async def checking_region(message: types.Message):
    user_text = message.text.lower()

    if user_text in INFO.region_titles:
        INFO.districts = INFO.regions[user_text]
        await choosing_district(message)
    else:
        await message.answer("Невідома область")
        await choosing_region(message, INFO.goal)


async def choosing_district(message: types.Message):
    markup = make_reply_keyboard_markup(width=2)
    districts_list = [district.capitalize()
                      for district in INFO.district_titles]
    markup.add(*districts_list)
    await message.answer("Виберіть район / міську (селищну) раду", reply_markup=markup)
    await Choosing.district.set()


@DP.message_handler(state=Choosing.district)
async def checking_district(message: types.Message):
    user_text = message.text.lower()

    if user_text in INFO.district_titles:
        INFO.district_letters = INFO.districts[user_text]
        await choosing_city_letter(message)
    else:
        await message.answer("Невідомий район / міська (селищна) рада")
        await choosing_district(message)


async def choosing_city_letter(message: types.Message):
    markup = make_reply_keyboard_markup(width=5)
    markup.add(*INFO.district_letters)
    await message.answer("Виберіть першу літеру міста / населеного пункту", reply_markup=markup)
    await Choosing.district_letter.set()


@DP.message_handler(state=Choosing.district_letter)
async def checking_city_letter(message: types.Message):
    user_text = message.text.upper()

    if user_text in INFO.district_letters:
        INFO.cities = INFO.district_letters[user_text]
        await choosing_city(message)
    else:
        await message.answer("Невідома перша літера")
        await choosing_city_letter(message)


async def choosing_city(message: types.Message):
    markup = make_reply_keyboard_markup(width=3)
    cities_list = [city.capitalize() for city in INFO.city_titles]
    markup.add(*cities_list)
    await message.answer("Виберіть місто / населений пункт", reply_markup=markup)
    await Choosing.city.set()


@DP.message_handler(state=Choosing.city)
async def checking_city(message: types.Message, state: FSMContext):
    user_text = message.text.lower()

    if user_text in INFO.city_titles:
        INFO.city = INFO.cities[user_text]

        if INFO.goal == "changing mailing":
            await state.finish()
            await change_mailing_city_by_(INFO.city, message)
        else:
            await choosing_period(message)
    else:
        await message.answer("Невідомий населений пункт")
        await choosing_city(message)


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

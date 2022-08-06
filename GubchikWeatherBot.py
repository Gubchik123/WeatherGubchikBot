import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import ClientSession

from config import TOKEN
from time import sleep
from random import random

REGIONS = {}
CITIES = {}

CITY = ""
TIME = ""
TYPE = "weather"

BOT = Bot(TOKEN)
DP = Dispatcher(BOT, storage=MemoryStorage())


class UserStep(StatesGroup):
    choosing_region = State()
    choosing_city = State()
    choosing_period = State()


@DP.message_handler(commands="start")
async def command_start(message: types.Message):
    sticker = "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    await message.answer_sticker(sticker)
    await message.answer(f"Привіт, {message.from_user.first_name}")
    await message.answer("Я той, хто допоможе тобі дізнатись погоду в містах України")

    await menu(message)


@DP.message_handler(commands="help")
async def command_help(message: types.Message):
    await message.answer("/weather - для перегляду прогнозу погоди\n"
                         "/moon - для перегляду фази місяця\n"
                         "Раджу використати кнопки для задуманого результату\n"
                         "Приємного використання!!!")
    sleep(random())
    await menu(message)


@DP.message_handler(commands="weather")
@DP.message_handler(Text(equals="переглянути прогноз погоди", ignore_case=True))
async def command_weather(message: types.Message):
    global CITY, TIME, TYPE

    CITY = ""
    TIME = ""
    TYPE = "weather"

    fill_regions_and_cities_dictionary_from_json()
    await choosing_region(message)


async def get_soup_by(url: str):
    async with ClientSession() as session:
        response = await session.get(url, headers={"user-agent": UserAgent().random})
        return BeautifulSoup(await response.text(), "lxml")


@DP.message_handler(commands="moon")
@DP.message_handler(Text(equals="переглянути фазу місяця", ignore_case=True))
async def get_info_about_moon(message: types.Message):
    url = "https://www.meteoprog.ua/ua/weather/Kharkiv/"

    try:
        soup = await get_soup_by(url)

        block = soup.find("div", class_="swiper-gallery")
        moon = block.find_all("li", class_="overall-day-info__item")[-1].find_all("div")[1].text.strip()
        moon = moon.replace("\n", ": ")

        await message.answer(moon)
        sleep(random())
        await menu(message)
    except Exception as error:
        await print_error(message, error)


def fill_regions_and_cities_dictionary_from_json():
    global REGIONS

    if len(REGIONS) == 0:
        with open("regions_and_cities.json", encoding="utf-8") as file:
            REGIONS = json.load(file)


async def print_error(message: types.Message, error):
    await message.answer("Виникла помилка! (Error)")
    await message.answer(str(error))


def make_reply_keyboard_markup(width: int, resize: bool):
    return types.ReplyKeyboardMarkup(row_width=width, resize_keyboard=resize)


def make_button(title: str):
    return types.KeyboardButton(title)


async def menu(message: types.Message):
    markup = make_reply_keyboard_markup(width=2, resize=True)
    markup.add(
        make_button("Переглянути прогноз погоди"),
        make_button("Переглянути фазу місяця"),
        make_button("Закінчити спілкування")
    )

    await message.answer("Виберіть подальші дії", reply_markup=markup)


def correct_title_from(title: str):
    if "Об" in title:
        return title.replace("Об", "об")
    elif "'Я" in title:
        return title.replace("'Я", "'я")
    else:
        return title


async def choosing_region(message: types.Message):
    markup = make_reply_keyboard_markup(width=2, resize=True)
    regions_list = [correct_title_from(region.title()) for region in REGIONS.keys()]
    markup.add(*regions_list)
    await message.answer("Виберіть область", reply_markup=markup)
    await UserStep.choosing_region.set()


@DP.message_handler(state=UserStep.choosing_region)
async def checking_region(message: types.Message):
    global CITIES

    user_text = message.text.lower()

    if user_text in REGIONS.keys():
        CITIES = REGIONS[user_text]
        await choosing_city(message)
    else:
        await message.answer("Невідома область")
        await choosing_region(message)


async def choosing_city(message: types.Message):
    markup = make_reply_keyboard_markup(width=3, resize=True)
    cities_list = [correct_title_from(city.title()) for city in CITIES.keys()]
    markup.add(*cities_list)
    await message.answer("Виберіть місто", reply_markup=markup)
    await UserStep.choosing_city.set()


@DP.message_handler(state=UserStep.choosing_city)
async def checking_city(message: types.Message):
    global CITY

    user_text = message.text.lower()

    if user_text in CITIES.keys():
        CITY = CITIES[user_text]
        await choosing_period(message)
    else:
        await message.answer("Невідоме місто")
        await choosing_city(message)


async def choosing_period(message: types.Message):
    markup = make_reply_keyboard_markup(width=2, resize=True)
    markup.add(
        make_button("Сьогодні"),
        make_button("Завтра"),
        make_button("Тиждень"),
        make_button("Два тижня")
    )

    await message.answer("Виберіть період прогнозу", reply_markup=markup)
    await UserStep.choosing_period.set()


def get_time_by_name(name: str):
    return {
        "сьогодні": lambda: "",
        "завтра": lambda: "tomorrow",
        "тиждень": lambda: "6_10",
        "два тижня": lambda: "review"
    }.get(name)()


@DP.message_handler(state=UserStep.choosing_period)
async def checking_period(message: types.Message, state: FSMContext):
    global TIME, TYPE

    user_text = message.text.lower()

    if user_text in ["сьогодні", "завтра", "тиждень", "два тижня"]:
        if get_time_by_name(user_text) == "review":
            TYPE = get_time_by_name(user_text)
        else:
            TIME = get_time_by_name(user_text)

        await get_data(message, state)
    else:
        await message.answer("Невідомий період прогнозу")
        await choosing_period(message)


def it_is_information_about_one_day():
    return TYPE == "weather" and TIME == "" or TIME == "tomorrow"


def it_is_information_about_many_days():
    return TYPE == "review" or TIME == "6_10"


async def get_data(message: types.Message, state: FSMContext):
    url = f"https://www.meteoprog.ua/ua/{TYPE}/{CITY}/{TIME}"

    try:
        soup = await get_soup_by(url)

        if it_is_information_about_one_day():
            await get_and_send_information_about_one_day(soup, message)
        elif it_is_information_about_many_days():
            await get_and_send_information_about_many_days(soup, message)

        await state.finish()
        await menu(message)
    except Exception as error:
        await print_error(message, error)


def get_block_and_title_from(soup: BeautifulSoup):
    block = soup.find("div", class_="page-columns-wrapper")
    title = block.find("h1").text.strip()

    return block, title


def time_today():
    return TIME == ""


async def get_and_send_information_about_one_day(soup: BeautifulSoup, message: types.Message):
    block, title = get_block_and_title_from(soup)

    if time_today():
        rain = block.find("table", class_="today__atmosphere").find_all("tr")[0].find("td").text.strip()
        wind = block.find("table", class_="today__atmosphere").find_all("tr")[1].find("td").text.strip()
        humidity = block.find("table", class_="today__atmosphere").find_all("tr")[4].find("td").text.strip()
    else:
        column3 = block.find("ul", class_="today-hourly-weather").find_all("li")[2]

        rain = column3.find("span", class_="precipitation-chance").text.strip()
        wind = column3.find("span", class_="wind-direction").text.strip()
        humidity = column3.find("span", class_="humidity").text.strip()

    await message.answer(f"{title}:\n\n"
                         f"Вітер: {wind}\n"
                         f"Вологість: {humidity}\n"
                         f"Імовірність опадів: {rain}")

    column = block.find("ul", class_="today-hourly-weather").find_all("li")

    name1 = column[0].find("span", class_="today-hourly-weather__name").text.strip()
    temp1 = column[0].find("span", class_="today-hourly-weather__temp").text.strip()
    desc1 = column[0].find("i", class_="today-hourly-weather__icon").get("title").strip()

    name2 = column[1].find("span", class_="today-hourly-weather__name").text.strip()
    temp2 = column[1].find("span", class_="today-hourly-weather__temp").text.strip()
    desc2 = column[1].find("i", class_="today-hourly-weather__icon").get("title").strip()

    name3 = column[2].find("span", class_="today-hourly-weather__name").text.strip()
    temp3 = column[2].find("span", class_="today-hourly-weather__temp").text.strip()
    desc3 = column[2].find("i", class_="today-hourly-weather__icon").get("title").strip()

    name4 = column[3].find("span", class_="today-hourly-weather__name").text.strip()
    temp4 = column[3].find("span", class_="today-hourly-weather__temp").text.strip()
    desc4 = column[3].find("i", class_="today-hourly-weather__icon").get("title").strip()

    await message.answer(f"{name1}: {temp1}\n({desc1})\n\n"
                         f"{name2}: {temp2}\n({desc2})\n\n"
                         f"{name3}: {temp3}\n({desc3})\n\n"
                         f"{name4}: {temp4}\n({desc4})\n\n")


async def get_and_send_information_about_many_days(soup: BeautifulSoup, message):
    block, title = get_block_and_title_from(soup)

    await message.answer(f"{title}:")

    all_details = block.find("div", class_="item-table").find_all("ul")

    block = block.find("div", class_="swiper-wrapper")
    all_days = block.find_all("div", class_="swiper-slide")

    for count, day in enumerate(all_days):
        name = day.find("div", class_="thumbnail-item__title").text.strip()
        date = day.find("div", class_="thumbnail-item__subtitle").text.strip()
        temp = day.find("div", class_="temperature-min").text.strip()

        wind = all_details[0].find_all("li")[count].text.strip()
        humidity = all_details[1].find_all("li")[count].text.strip()
        rain = all_details[3].find_all("li")[count].text.strip()

        block_with_details = soup.find("div", class_="swiper-gallery")
        description = block_with_details.find_all("div", class_="description")[count].text.strip()
        description = description.split(": ")[1]

        await message.answer(f"{name} ({date}): {temp}\n"
                             f"{description}\n\n"
                             f"Вітер: {wind}\n"
                             f"Вологість: {rain}\n"
                             f"Імовірність опадів: {humidity}\n")
        sleep(0.5)


@DP.message_handler(Text(equals="закінчити спілкування", ignore_case=True))
async def the_end(message: types.Message):
    sticker = "CAACAgIAAxkBAAICBGLIifDJ3jPz291sEcRKE5EO4j99AALsAwAC0lqIAZ0zny94Yp4oKQQ"

    markup = make_reply_keyboard_markup(width=1, resize=True)
    markup.add(make_button("/start"))

    await message.answer_sticker(sticker)
    await message.answer(f"Бувай, {message.from_user.first_name}, повертайся ще\n"
                         "Наступного разу просто введи або натисни /start :)", reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(DP)

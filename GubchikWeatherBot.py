import json
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from telebot import TeleBot
from telebot import types
from config import TOKEN

from time import sleep
from random import random

REGIONS = {}
CITIES = {}

CITY = ""
TIME = ""
TYPE = "weather"
BOT = TeleBot(TOKEN)


@BOT.message_handler(commands=["start"])
def command_start(message):
    sticker = "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    BOT.send_sticker(message.chat.id, sticker)
    BOT.send_message(message.chat.id, f"Привіт, {message.from_user.first_name}")
    BOT.send_message(message.chat.id, "Я той, хто допоможе тобі дізнатись погоду в містах України")

    menu(message)


@BOT.message_handler(commands=["help"])
def command_help(message):
    BOT.send_message(message.chat.id, "/weather - для перегляду прогнозу погоди")
    BOT.send_message(message.chat.id, "/moon - для перегляду фази місяця")
    BOT.send_message(message.chat.id, "Раджу використати кнопки для задуманого результату")
    BOT.send_message(message.chat.id, "Приємного використання!!!")
    sleep(random())
    menu(message)


@BOT.message_handler(commands=["weather"])
def command_weather(message):
    global CITY, TIME, TYPE

    CITY = ""
    TIME = ""
    TYPE = "weather"

    fill_regions_and_cities_dictionary_from_json()
    choosing_region(message)


@BOT.message_handler(commands=["moon"])
def get_info_about_moon(message):
    url = "https://www.meteoprog.ua/ua/weather/Kharkiv/"

    try:
        response = requests.get(url, headers={"user-agent": UserAgent().random})
        soup = BeautifulSoup(response.text, "lxml")

        block = soup.find("div", class_="swiper-gallery")
        moon = block.find_all("li", class_="overall-day-info__item")[-1].find_all("div")[1].text.strip()
        moon = moon.replace("\n", ": ")

        BOT.send_message(message.chat.id, moon)
        sleep(random())
        menu(message)
    except Exception as error:
        print_error(message, error)


def fill_regions_and_cities_dictionary_from_json():
    global REGIONS

    if len(REGIONS) == 0:
        with open("regions_and_cities.json", encoding="utf-8") as file:
            REGIONS = json.load(file)


def print_error(message, error):
    BOT.send_message(message.chat.id, "Виникла помилка! (Error)")
    BOT.send_message(message.chat.id, str(error))


def make_reply_keyboard_markup(width: int, resize: bool):
    return types.ReplyKeyboardMarkup(row_width=width, resize_keyboard=resize)


def make_button(title: str):
    return types.KeyboardButton(title)


def menu(message):
    markup = make_reply_keyboard_markup(width=2, resize=True)
    markup.add(
        make_button("Переглянути прогноз погоди"),
        make_button("Переглянути фазу місяця"),
        make_button("Закінчити спілкування")
    )

    BOT.send_message(message.chat.id, "Виберіть подальші дії", reply_markup=markup)
    BOT.register_next_step_handler(message, checking_answer_from_menu)


def user_want_to_know_about_weather(user_text):
    return user_text == "/weather" or user_text == "переглянути прогноз погоди"


def user_want_to_know_about_moon(user_text):
    return user_text == "/moon" or user_text == "переглянути фазу місяця"


def checking_answer_from_menu(message):
    user_text = message.text.lower()

    if user_text == "/start":
        command_start(message)
    elif user_text == "/help":
        command_help(message)
    elif user_want_to_know_about_weather(user_text):
        command_weather(message)
    elif user_want_to_know_about_moon(user_text):
        get_info_about_moon(message)
    elif user_text == "закінчити спілкування":
        the_end(message)
    else:
        BOT.send_message(message.chat.id, "Вибачте, я не знаю такої команди")
        menu(message)


def correct_title_from(title: str):
    if "О" in title.split()[-1]:
        return title.split()[0] + ' ' + title.split()[-1].replace("О", "о")
    elif "'Я" in title:
        return title.replace("'Я", "'я")
    else:
        return title


def choosing_region(message):
    markup = make_reply_keyboard_markup(width=2, resize=True)
    for region in REGIONS.keys():
        markup.add(
            make_button(correct_title_from(region.title()))
        )

    BOT.send_message(message.chat.id, "Виберіть область", reply_markup=markup)
    BOT.register_next_step_handler(message, checking_region)


def checking_region(message):
    global CITIES

    user_text = message.text.lower()

    if user_text in REGIONS.keys():
        CITIES = REGIONS[user_text]
        choosing_city(message)
    else:
        BOT.send_message(message.chat.id, "Невідома область")
        choosing_region(message)


def choosing_city(message):
    markup = make_reply_keyboard_markup(width=2, resize=True)
    for city in CITIES.keys():
        markup.add(
            make_button(correct_title_from(city.title()))
        )

    BOT.send_message(message.chat.id, "Выберите город", reply_markup=markup)
    BOT.register_next_step_handler(message, checking_city)


def checking_city(message):
    global CITY

    user_text = message.text.lower()

    if user_text in CITIES.keys():
        CITY = CITIES[user_text]
        choosing_period(message)
    else:
        BOT.send_message(message.chat.id, "Невідоме місто")
        choosing_city(message)


def choosing_period(message):
    markup = make_reply_keyboard_markup(width=2, resize=True)
    markup.add(
        make_button("Сьогодні"),
        make_button("Завтра"),
        make_button("Тиждень"),
        make_button("Два тижня")
    )

    BOT.send_message(message.chat.id, "Виберіть період прогнозу", reply_markup=markup)
    BOT.register_next_step_handler(message, checking_period)


def get_time_by_name(name: str):
    return {
        "сьогодні": lambda: "",
        "завтра": lambda: "tomorrow",
        "тиждень": lambda: "6_10",
        "два тижня": lambda: "review"
    }.get(name)()


def checking_period(message):
    global TIME, TYPE

    user_text = message.text.lower()

    if user_text in ["сьогодні", "завтра", "тиждень", "два тижня"]:
        if get_time_by_name(user_text) == "review":
            TYPE = get_time_by_name(user_text)
        else:
            TIME = get_time_by_name(user_text)

        get_data(message)
    else:
        BOT.send_message(message.chat.id, "Невідомий період прогнозу")
        choosing_period(message)


def it_is_information_about_one_day():
    return TYPE == "weather" and TIME == "" or TIME == "tomorrow"


def it_is_information_about_many_days():
    return TYPE == "review" or TIME == "6_10"


def get_data(message):
    url = f"https://www.meteoprog.ua/ua/{TYPE}/{CITY}/{TIME}"

    try:
        response = requests.get(url, headers={"user-agent": UserAgent().random})
        soup = BeautifulSoup(response.text, "lxml")

        if it_is_information_about_one_day():
            get_and_send_information_about_one_day(soup, message)
        elif it_is_information_about_many_days():
            get_and_send_information_about_many_days(soup, message)

        menu(message)
    except Exception as error:
        print_error(message, error)


def get_block_and_title_from(soup: BeautifulSoup):
    block = soup.find("div", class_="page-columns-wrapper")
    title = block.find("h1").text.strip()

    return block, title


def time_today():
    return TIME == ""


def get_and_send_information_about_one_day(soup: BeautifulSoup, message):
    block, title = get_block_and_title_from(soup)

    description = block.find("h3").text.strip()

    if time_today():
        wind = block.find("table", class_="today__atmosphere").find_all("tr")[1].find("td").text.strip()
    else:
        column3 = block.find("ul", class_="today-hourly-weather").find_all("li")[2]
        wind = column3.find("span", class_="wind-direction").text.strip()

    BOT.send_message(message.chat.id, f"{title}:")
    BOT.send_message(message.chat.id, f"{description} (Вітер: {wind})")

    columns = block.find("ul", class_="today-hourly-weather").find_all("li")
    for column in columns:
        name = column.find("span", class_="today-hourly-weather__name").text.strip()
        temp = column.find("span", class_="today-hourly-weather__temp").text.strip()

        BOT.send_message(message.chat.id, f"{name}: {temp}")
        sleep(random())


def get_and_send_information_about_many_days(soup: BeautifulSoup, message):
    block, title = get_block_and_title_from(soup)

    BOT.send_message(message.chat.id, f"{title}:")

    block = block.find("div", class_="swiper-wrapper")
    all_days = block.find_all("div", class_="swiper-slide")

    for count, day in enumerate(all_days):
        name = day.find("div", class_="thumbnail-item__title").text.strip()
        date = day.find("div", class_="thumbnail-item__subtitle").text.strip()
        temp = day.find("div", class_="temperature-min").text.strip()

        block_with_details = soup.find("div", class_="swiper-gallery")
        description = block_with_details.find_all("div", class_="description")[count].text.strip()
        description = description.split(": ")[1]

        BOT.send_message(message.chat.id, f"{name} ({date}): {temp}; {description}")
        sleep(random())


def the_end(message):
    markup = make_reply_keyboard_markup(width=1, resize=True)
    markup.add(make_button("/start"))

    sticker = "CAACAgIAAxkBAAICBGLIifDJ3jPz291sEcRKE5EO4j99AALsAwAC0lqIAZ0zny94Yp4oKQQ"

    BOT.send_sticker(message.chat.id, sticker)
    BOT.send_message(message.chat.id, f"Бувай, {message.from_user.first_name}, повертайся ще")
    BOT.send_message(message.chat.id, "Наступного разу просто введи або натисни /start :)", reply_markup=markup)


BOT.polling()

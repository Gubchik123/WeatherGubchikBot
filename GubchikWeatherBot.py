import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from telebot import TeleBot
from telebot import types
from config import TOKEN

from time import sleep
from random import random

CITY = ""
TIME = ""
TYPE = "weather"
BOT = TeleBot(TOKEN)


@BOT.message_handler(commands=["start"])
def command_start(message):
    sticker = "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    BOT.send_sticker(message.chat.id, sticker)
    BOT.send_message(message.chat.id, f"Привет, {message.from_user.first_name}")
    BOT.send_message(message.chat.id, "Я тот, кто поможет тебе узнать погоду в городах Украины")

    menu(message)


@BOT.message_handler(commands=["help"])
def command_help(message):
    BOT.send_message(message.chat.id, "/weather - для просмотра прогноза погоды")
    BOT.send_message(message.chat.id, "/moon - для просмотра фазы луны")
    BOT.send_message(message.chat.id, "Советую использовать кнопки для задуманого результата")
    BOT.send_message(message.chat.id, "Приятного использования!!!")
    sleep(random())
    menu(message)


@BOT.message_handler(commands=["weather"])
def command_weather(message):
    global CITY, TIME, TYPE
    CITY = ""
    TIME = ""
    TYPE = "weather"

    choosing_city(message)


@BOT.message_handler(commands=["moon"])
def get_info_about_moon(message):
    url = "https://www.meteoprog.ua/ru/weather/Kharkiv/"

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


def print_error(message, error):
    BOT.send_message(message.chat.id, "Возникла ошибка! (Error)")
    BOT.send_message(message.chat.id, str(error))


def make_reply_keyboard_markup(row_width: int, resize: bool):
    return types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize)


def make_button(title: str):
    return types.KeyboardButton(title)


def menu(message):
    markup = make_reply_keyboard_markup(row_width=2, resize=True)
    markup.add(
        make_button("Посмотреть прогноз погоды"),
        make_button("Посмотреть фазу луны"),
        make_button("Закончить общение")
    )

    BOT.send_message(message.chat.id, "Выберите дальнейшие действия", reply_markup=markup)
    BOT.register_next_step_handler(message, checking_answer_from_menu)


def checking_answer_from_menu(message):
    user_text = message.text.lower()

    if user_text == "/start":
        command_start(message)
    elif user_text == "/help":
        command_help(message)
    elif user_text == "/weather":
        command_weather(message)
    elif user_text == "/moon":
        get_info_about_moon(message)
    elif user_text == "посмотреть прогноз погоды":
        choosing_city(message)
    elif user_text == "посмотреть фазу луны":
        get_info_about_moon(message)
    elif user_text == "закончить общение":
        the_end(message)
    else:
        BOT.send_message(message.chat.id, "Извините, я не знаю такой команды")
        menu(message)


def get_city_name_by_name(name: str):
    return {
        "харьков": lambda: "Kharkiv",
        "полтава": lambda: "Poltava",
        "красноград": lambda: "Krasnograd",
        "днепр": lambda: "Dnipropetrovsk",
        "киев": lambda: "Kyiv",
        "львов": lambda: "Lviv",
    }.get(name, lambda: "Unknown")()


def get_time_by_name(name: str):
    return {
        "сегодня": lambda: "",
        "завтра": lambda: "tomorrow",
        "неделя": lambda: "6_10",
        "две недели": lambda: "review"
    }.get(name, lambda: "Unknown")()


def choosing_city(message):
    markup = make_reply_keyboard_markup(row_width=3, resize=True)
    markup.add(
        make_button("Харьков"),
        make_button("Полтава"),
        make_button("Красноград"),
        make_button("Днепр"),
        make_button("Киев"),
        make_button("Львов")
    )

    BOT.send_message(message.chat.id, "Выберите город", reply_markup=markup)
    BOT.register_next_step_handler(message, checking_city)


def checking_city(message):
    global CITY

    user_text = message.text.lower()

    if user_text in ["харьков", "полтава", "красноград", "киев", "львов", "днепр"]:
        CITY = get_city_name_by_name(user_text)
        choosing_period(message)
    else:
        BOT.send_message(message.chat.id, "Неизвестный город")
        choosing_city(message)


def choosing_period(message):
    markup = make_reply_keyboard_markup(row_width=2, resize=True)
    markup.add(
        make_button("Сегодня"),
        make_button("Завтра"),
        make_button("Неделя"),
        make_button("Две недели")
    )

    BOT.send_message(message.chat.id, "Выберите период прогноза", reply_markup=markup)
    BOT.register_next_step_handler(message, checking_period)


def checking_period(message):
    global TIME, TYPE

    user_text = message.text.lower()

    if user_text in ["сегодня", "завтра", "неделя", "две недели"]:
        if get_time_by_name(user_text) == "review":
            TYPE = get_time_by_name(user_text)
        else:
            TIME = get_time_by_name(user_text)

        get_data(message)
    else:
        BOT.send_message(message.chat.id, "Неизвестный период")
        choosing_period(message)


def it_is_information_about_one_day():
    return TYPE == "weather" and TIME == "" or TIME == "tomorrow"


def it_is_information_about_many_days():
    return TYPE == "review" or TIME == "6_10"


def get_data(message):
    url = f"https://www.meteoprog.ua/ru/{TYPE}/{CITY}/{TIME}"

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
    BOT.send_message(message.chat.id, f"{description} (Ветер: {wind})")

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
    markup = make_reply_keyboard_markup(row_width=1, resize=True)
    markup.add(make_button("/start"))

    sticker = "CAACAgIAAxkBAAICBGLIifDJ3jPz291sEcRKE5EO4j99AALsAwAC0lqIAZ0zny94Yp4oKQQ"

    BOT.send_sticker(message.chat.id, sticker)
    BOT.send_message(message.chat.id, f"Пока, {message.from_user.first_name}, возращайся ещё")
    BOT.send_message(message.chat.id, "В следующий раз просто введи или нажми /start :)", reply_markup=markup)


BOT.polling()

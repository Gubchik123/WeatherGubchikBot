from typing import NamedTuple

from aiogram import types
from bs4 import BeautifulSoup

from bot_info import BOT
from constants import INFO, TEXT

from ..menu import menu
from .getting_emoji import get_weather_emoji_by_
from .general import get_soup_by_, send_message_to_user_about_error


class WeatherDetail(NamedTuple):
    wind: str
    rain: str
    humidity: str


class WeatherDetailTitle(WeatherDetail):
    pass


async def get_info_about_weather_by_(message: types.Message):
    try:
        await message.answer(
            get_information_about_one_day()
            if INFO.about_one_day
            else get_information_about_many_days()
        )

        if message.from_user.id != 1065489646:
            await BOT.send_message(
                1065489646,
                f"{message.from_user.first_name} weather in {INFO.city_title} ({INFO.time_title})",
            )

        await menu(message)
    except Exception as error:
        await send_message_to_user_about_error(message, error)


def get_block_and_title_from(soup: BeautifulSoup):
    try:
        block = soup.find("div", class_="page-columns-wrapper")
        return (block, block.find("h1").text.strip())
    except AttributeError:
        return get_block_and_title_from(get_soup_by_(INFO.generated_url))


def get_atmosphere_row(index: int, block: BeautifulSoup) -> str:
    return (
        block.find("table", class_="today__atmosphere")
        .find_all("tr")[index]
        .find("td")
        .text.strip()
    )


def get_all_columns_from_(block: BeautifulSoup):
    return block.find("ul", class_="today-hourly-weather").find_all("li")


def get_span_text_from_(column: BeautifulSoup, class_: str) -> str:
    return column.find("span", class_=class_).text.strip()


def get_span_number_from_(column: BeautifulSoup, class_: str) -> str:
    span_text = get_span_text_from_(column, class_)
    return span_text.split(" ")[0] if " " in span_text else span_text[:-1]


def get_wind_symbol():
    return {"uk": "м/с", "en": "mps", "ru": "м/с"}.get(TEXT().lang_code)


def get_weather_details_on_one_day_from_(block: BeautifulSoup) -> WeatherDetail:
    global INFO

    if INFO.about_today:
        return WeatherDetail(
            rain=get_atmosphere_row(0, block),
            wind=get_atmosphere_row(1, block),
            humidity=get_atmosphere_row(4, block),
        )

    # if selected time is tomorrow
    rain, wind, humidity = 0, 0, 0
    for column in get_all_columns_from_(block):
        rain += int(get_span_number_from_(column, class_="precipitation-chance"))
        wind += int(get_span_number_from_(column, class_="wind-direction"))
        humidity += int(get_span_number_from_(column, class_="humidity"))

    return WeatherDetail(
        rain=f"{int(rain/4)} %",
        wind=f"{int(wind/4)} {get_wind_symbol()}",
        humidity=f"{int(humidity/4)} %",
    )


def get_weather_detail_titles() -> WeatherDetailTitle:
    return {
        "uk": WeatherDetailTitle(
            rain="Імовірність опадів", wind="Вітер", humidity="Вологість"
        ),
        "ru": WeatherDetailTitle(
            rain="Возможность осадков", wind="Ветер", humidity="Влажность"
        ),
        "en": WeatherDetailTitle(
            rain="Chance of precipitation", wind="Wind", humidity="Humidity"
        ),
    }.get(TEXT().lang_code)


def get_weather_info_about_day_from_(block: BeautifulSoup) -> str:
    text = ""

    column = block.find("ul", class_="today-hourly-weather").find_all("li")

    for count in range(4):
        name = get_span_text_from_(column[count], class_="today-hourly-weather__name")
        temp = get_span_text_from_(column[count], class_="today-hourly-weather__temp")
        desc = (
            column[count]
            .find("i", class_="today-hourly-weather__icon")
            .get("title")
            .strip()
        )

        text += f"\n{name}: {temp}  {get_weather_emoji_by_(desc)}\n({desc})\n"

    return text


def get_information_about_one_day():
    block, title = get_block_and_title_from(get_soup_by_(INFO.generated_url))

    weather_detail_titles = get_weather_detail_titles()
    weather_details = get_weather_details_on_one_day_from_(block)

    return f"""
    {title}:

    {weather_detail_titles.wind}: {weather_details.wind}  🌬
    {weather_detail_titles.humidity}: {weather_details.humidity}  💦
    {weather_detail_titles.rain}: {weather_details.rain}  💧
    {get_weather_info_about_day_from_(block)}
    """.replace(
        "    ", ""
    )


def get_div_text_from_(block: BeautifulSoup, class_: str) -> str:
    return block.find("div", class_=class_).text.strip()


def get_information_about_many_days():
    text = ""
    soup = get_soup_by_(INFO.generated_url)
    block, title = get_block_and_title_from(soup)

    text += f"{title}:"

    weather_detail_titles = get_weather_detail_titles()
    all_details = block.find("div", class_="item-table").find_all("ul")

    block = block.find("div", class_="swiper-wrapper")
    all_days = block.find_all("div", class_="swiper-slide")

    for count, day in enumerate(all_days):
        name = get_div_text_from_(day, class_="thumbnail-item__title")
        date = get_div_text_from_(day, class_="thumbnail-item__subtitle")
        temp = get_div_text_from_(day, class_="temperature-min")

        wind_info = all_details[0].find_all("li")[count].text.strip()
        humidity_info = all_details[1].find_all("li")[count].text.strip()
        rain_info = all_details[3].find_all("li")[count].text.strip()

        block_with_details = soup.find("div", class_="swiper-gallery")
        description = block_with_details.find_all("div", class_="description")[
            count
        ].text.strip()
        description = description.split(": ")[1]

        text += f"""
        
        {name} ({date}): {temp}  {get_weather_emoji_by_(description)}
        {description}

        {weather_detail_titles.wind}: {wind_info}  🌬
        {weather_detail_titles.humidity}: {humidity_info}  💦
        {weather_detail_titles.rain}: {rain_info}  💧
        {"_"*35}""".replace(
            "        ", ""
        )

    return text

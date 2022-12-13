from typing import NamedTuple

from aiogram import types
from bs4 import BeautifulSoup

from bot_info import BOT
from constants import INFO, TEXT

from ..menu import menu
from .getting_emoji import get_weather_emoji_by_
from .general import get_soup_by_, send_message_to_user_about_error


class WeatherDetail(NamedTuple):
    """For storing weather details after parsing"""
    wind: str
    rain: str
    humidity: str


class WeatherDetailTitle(WeatherDetail):
    """For storing weather detail titles by language"""
    pass


async def get_info_about_weather_by_(message: types.Message):
    """For sending weather message to user"""
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
    """For getting block for future parsing and page title (h1)"""
    try:
        block = soup.find("div", class_="page-columns-wrapper")
        return (block, block.find("h1").text.strip())
    except AttributeError:
        return get_block_and_title_from(get_soup_by_(INFO.generated_url))


def get_atmosphere_row(index: int, block: BeautifulSoup) -> str:
    """For getting parsed row from table by index"""
    return (
        block.find("table", class_="today__atmosphere")
        .find_all("tr")[index]
        .find("td")
        .text.strip()
    )


def get_all_columns_from_(block: BeautifulSoup):
    """For getting all list items with weather data"""
    return block.find("ul", class_="today-hourly-weather").find_all("li")


def get_span_text_from_(column: BeautifulSoup, class_: str) -> str:
    """For getting span text from column by class CSS selector"""
    return column.find("span", class_=class_).text.strip()


def get_span_number_from_(column: BeautifulSoup, class_: str) -> str:
    """For getting span number from column by class CSS selector"""
    span_text = get_span_text_from_(column, class_)
    return span_text.split(" ")[0] if " " in span_text else span_text[:-1]


def get_wind_symbol():
    """For getting wind symbol by current language code"""
    return {"uk": "м/с", "en": "mps", "ru": "м/с"}.get(TEXT().lang_code)


def get_weather_details_on_one_day_from_(block: BeautifulSoup) -> WeatherDetail:
    """For checking if period is today or tomorrow and getting weather details"""
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
        rain += int(get_span_number_from_(column,
                    class_="precipitation-chance"))
        wind += int(get_span_number_from_(column, class_="wind-direction"))
        humidity += int(get_span_number_from_(column, class_="humidity"))

    return WeatherDetail(
        rain=f"{int(rain/4)} %",
        wind=f"{int(wind/4)} {get_wind_symbol()}",
        humidity=f"{int(humidity/4)} %",
    )


def get_weather_detail_titles() -> WeatherDetailTitle:
    """For getting weather detail titles by current language code"""
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
    """For getting text with weather information about one day"""
    text = ""

    column = block.find("ul", class_="today-hourly-weather").find_all("li")

    for count in range(4):
        name = get_span_text_from_(
            column[count], class_="today-hourly-weather__name")
        temp = get_span_text_from_(
            column[count], class_="today-hourly-weather__temp")
        desc = (
            column[count]
            .find("i", class_="today-hourly-weather__icon")
            .get("title")
            .strip()
        )

        text += f"\n{name}: {temp}  {get_weather_emoji_by_(desc)}\n({desc})\n"

    return text


def get_information_about_one_day():
    """For getting result weather message about one day"""
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


def get_weather_details_on_many_days_from_(block: BeautifulSoup, count: int):
    return WeatherDetail(
        wind=block[0].find_all("li")[count].text.strip(),
        humidity=block[1].find_all("li")[count].text.strip(),
        rain=block[3].find_all("li")[count].text.strip(),
    )


def get_description_from_(block: BeautifulSoup, count: int):
    block_with_details = block.find("div", class_="swiper-gallery")
    description = block_with_details.find_all("div", class_="description")[
        count
    ].text.strip()
    return description.split(": ")[1]


def get_div_text_from_(block: BeautifulSoup, class_: str) -> str:
    """For getting text from block (div) by class CSS selector"""
    return block.find("div", class_=class_).text.strip()


def get_information_about_many_days():
    """For getting result weather message about many days"""
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

        weather_details = get_weather_details_on_many_days_from_(
            all_details, count
        )
        description = get_description_from_(soup, count)

        text += f"""
        
        {name} ({date}): {temp}  {get_weather_emoji_by_(description)}
        {description}

        {weather_detail_titles.wind}: {weather_details.wind}  🌬
        {weather_detail_titles.humidity}: {weather_details.humidity}  💦
        {weather_detail_titles.rain}: {weather_details.rain}  💧
        {"_"*35}""".replace(
            "        ", ""
        )

    return text

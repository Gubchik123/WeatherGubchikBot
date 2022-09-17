from aiogram import types
from bs4 import BeautifulSoup

from constants import INFO, TEXT

from ..menu import menu
from .get_emoji import get_weather_emoji_by_
from .general import get_soup_by_, send_message_to_user_about_error


async def get_info_about_weather_by_(message: types.Message):
    try:
        soup = get_soup_by_(INFO.generated_url)

        if INFO.about_one_day:
            await message.answer(get_information_about_one_day(soup))
        elif INFO.about_many_days:
            await message.answer(get_information_about_many_days(soup))

        await menu(message)
    except Exception as error:
        await send_message_to_user_about_error(message, error)


def get_block_and_title_from(soup: BeautifulSoup):
    block = soup.find("div", class_="page-columns-wrapper")
    title = block.find("h1").text.strip()

    return (block, title)


def get_atmosphere_row(index: int, block: BeautifulSoup) -> str:
    return block.find(
        "table",
        class_="today__atmosphere"
    ).find_all("tr")[index].find("td").text.strip()


def get_span_text_from_(column: BeautifulSoup, class_: str) -> str:
    return column.find("span", class_=class_).text.strip()


def get_rain_wind_and_humidity_on_one_day_from_(block: BeautifulSoup):
    global INFO

    if INFO.about_today:
        rain = get_atmosphere_row(0, block)
        wind = get_atmosphere_row(1, block)
        humidity = get_atmosphere_row(4, block)
    else:  # if selected time is tomorrow
        column3 = block.find(
            "ul", class_="today-hourly-weather").find_all("li")[2]

        rain = get_span_text_from_(column3, class_="precipitation-chance")
        wind = get_span_text_from_(column3,  class_="wind-direction")
        humidity = get_span_text_from_(column3,  class_="humidity")

    return (rain, wind, humidity)


def get_rain_wind_and_humidity_title_by_():
    return {
        "uk": ("Імовірність опадів", "Вітер", "Вологість"),
        "ru": ("Возможность осадков", "Ветер", "Влажность"),
        "en": ("Chance of precipitation", "Wind", "Humidity"),
    }.get(TEXT.lang_code)


def get_weather_info_about_day_from_(block: BeautifulSoup) -> str:
    text = ""

    column = block.find("ul", class_="today-hourly-weather").find_all("li")

    for count in range(4):
        name = get_span_text_from_(column[count],
                                   class_="today-hourly-weather__name")
        temp = get_span_text_from_(column[count],
                                   class_="today-hourly-weather__temp")
        desc = column[count].find(
            "i",
            class_="today-hourly-weather__icon"
        ).get("title").strip()

        text += f"\n{name}: {temp}  {get_weather_emoji_by_(desc)}\n({desc})\n"

    return text


def get_information_about_one_day(soup: BeautifulSoup):
    text = ""
    block, title = get_block_and_title_from(soup)

    rain_title, wind_title, humidity_title = \
        get_rain_wind_and_humidity_title_by_()

    rain_info, wind_info, humidity_info = \
        get_rain_wind_and_humidity_on_one_day_from_(block)

    text += f"""
    {title}:

    {wind_title}: {wind_info}  🌬
    {humidity_title}: {humidity_info}  💦
    {rain_title}: {rain_info}  💧
    """.replace("    ", "")

    text += get_weather_info_about_day_from_(block)
    return text


def get_div_text_from_(block: BeautifulSoup, class_: str) -> str:
    return block.find("div", class_=class_).text.strip()


def get_information_about_many_days(soup: BeautifulSoup):
    text = ""
    block, title = get_block_and_title_from(soup)

    text += f"{title}:"

    rain_title, wind_title, humidity_title = \
        get_rain_wind_and_humidity_title_by_()

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
        description = block_with_details.find_all(
            "div", class_="description")[count].text.strip()
        description = description.split(": ")[1]

        text += f"""
        
        {name} ({date}): {temp}  {get_weather_emoji_by_(description)}
        {description}

        {wind_title}: {wind_info}  🌬
        {humidity_title}: {humidity_info}  💦
        {rain_title}: {rain_info}  💧
        {"_"*35}""".replace("        ", "")

    return text

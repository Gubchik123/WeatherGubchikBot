from time import sleep
from emoji import emojize
from bs4 import BeautifulSoup
from aiogram import types

from .general import get_soup_by, print_error
from .get_emoji import get_weather_emoji_by_
from ..menu import menu

from utils.class_SelectedInfo import SelectedInfo


async def get_info_about_weather_by_(info: SelectedInfo, message: types.Message):
    try:
        soup = get_soup_by(info.generated_url)

        if info.about_one_day:
            await message.answer(get_information_about_one_day(soup, info))
        elif info.about_many_days:
            await message.answer(get_and_send_information_about_many_days(soup))

        await menu(message)
    except Exception as error:
        await print_error(message, error)


def get_block_and_title_from(soup: BeautifulSoup):
    block = soup.find("div", class_="page-columns-wrapper")
    title = block.find("h1").text.strip()

    return block, title


def get_information_about_one_day(soup: BeautifulSoup, info: SelectedInfo):
    text = ""
    block, title = get_block_and_title_from(soup)

    if info.about_today:
        rain = block.find("table", class_="today__atmosphere").find_all("tr")[
            0].find("td").text.strip()
        wind = block.find("table", class_="today__atmosphere").find_all("tr")[
            1].find("td").text.strip()
        humidity = block.find("table", class_="today__atmosphere").find_all("tr")[
            4].find("td").text.strip()
    else:
        column3 = block.find(
            "ul", class_="today-hourly-weather").find_all("li")[2]

        rain = column3.find("span", class_="precipitation-chance").text.strip()
        wind = column3.find("span", class_="wind-direction").text.strip()
        humidity = column3.find("span", class_="humidity").text.strip()

    text += f"""
    {title}:

Вітер: {wind}  {emojize(':wind_face:')}
Вологість: {humidity}  {emojize(':sweat_droplets:')}
Імовірність опадів: {rain}  {emojize(':droplet:')}
    """

    column = block.find("ul", class_="today-hourly-weather").find_all("li")

    for count in range(4):
        name = column[count].find(
            "span", class_="today-hourly-weather__name").text.strip()
        temp = column[count].find(
            "span", class_="today-hourly-weather__temp").text.strip()
        desc = column[count].find(
            "i", class_="today-hourly-weather__icon").get("title").strip()

        text += f"\n{name}: {temp}  {get_weather_emoji_by_(desc)}\n({desc})\n"

    return text


def get_and_send_information_about_many_days(soup: BeautifulSoup):
    text = ""
    block, title = get_block_and_title_from(soup)

    text += f"{title}:\n"

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
        description = block_with_details.find_all(
            "div", class_="description")[count].text.strip()
        description = description.split(": ")[1]

        text += f"\n{name} ({date}): {temp}  {get_weather_emoji_by_(description)}\n"
        text += f"{description}\n\n"
        text += f"Вітер: {wind}  {emojize(':wind_face:')}\n"
        text += f"Вологість: {humidity}  {emojize(':sweat_droplets:')}\n"
        text += f"Імовірність опадів: {rain}  {emojize(':droplet:')}\n"
        text += "\n" + "-"*70 + "\n"

    return text

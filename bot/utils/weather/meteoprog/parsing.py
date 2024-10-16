from typing import Dict, Optional

from bs4 import BeautifulSoup
from aiogram.utils.i18n import gettext as _

from .selected_info import SelectedInfo

from ..request import get_soup_by_
from ..emoji import get_weather_emoji_by_


INFO = SelectedInfo()

MAX_TEMPS: Dict[str, int] = {}
MIN_TEMPS: Dict[str, int] = {}


def get_information_about_weather_by_(data: dict) -> str:
    """For getting result weather message about weather"""
    INFO.set(**data)

    if INFO.about_now:
        return get_information_for_now()
    elif INFO.about_one_day:
        return get_information_about_one_day()
    return get_information_about_many_days()


def get_information_for_now() -> str:
    """For getting result weather message for now."""
    soup = get_soup_by_(INFO.generated_url, INFO.lang_code)
    return _get_weather_info_for_now_from_(soup)


def _get_weather_info_for_now_from_(soup: BeautifulSoup) -> str:
    """For getting weather message for now."""
    block = soup.find("section", class_="today-block")
    # Temperature
    temp = (
        block.find("div", class_="today-temperature").find("span").text.strip()
    )
    feels_like = (
        block.find("span", class_="feels-like")
        .text.strip()
        .replace("°C ", "°C (")
        + ")"
    )
    # Description
    desc = block.find("h3").text.strip()
    # Details
    details = block.find("table", class_="today__atmosphere").find_all("tr")

    text = (
        f"<b>{block.find('h2').text.strip()}</b>\n\n"
        f"{temp}C {get_weather_emoji_by_(desc, INFO.lang_code)}\n"
        f"{feels_like}\n\n"
        f"{desc}\n<blockquote expandable>"
    )
    for detail in details:
        td = detail.find("td")
        icon = _get_weather_detail_icon_by_(td.find("span").get("class")[0])
        text += (
            f"<i>{detail.find('th').text.strip()}:</i> "
            f"{td.text.strip()} {icon}\n"
        )
    return f"{text}</blockquote>"


def _get_weather_detail_icon_by_(icon_css_class: str) -> str:
    return {
        "icon-rain-drops": "💦",
        "icon-waves": "🌂",
        "icon-rainfall": "🌂",
        "icon-wind": "🌬️",
        "icon-wind-left": "⬅️🌬️",
        "icon-wind-bottom-left": "↙️🌬️",
        "icon-wind-right": "➡️🌬️",
        "icon-wind-bottom-right": "↘️🌬️",
        "icon-wind-top-left": "↖️🌬️",
        "icon-wind-top-right": "↗️🌬️",
        "icon-wind-bottom": "⬇️🌬️",
        "icon-wind-top": "⬆️🌬️",
        "icon-dropp": "💧",
        "icon-meater": "🌡️",
        "icon-uv": "📉",
    }.get(icon_css_class, "")


def get_information_about_one_day() -> str:
    """For getting result weather message about one day"""
    soup = get_soup_by_(INFO.generated_url, INFO.lang_code)
    active_swiper_slide = get_active_swiper_slide_from(soup)
    return (
        f"<b>{get_one_day_title(soup)}</b>\n\n"
        f"{get_weather_info_about_day_from_(active_swiper_slide)}"
    )


def get_information_about_many_days() -> str:
    MAX_TEMPS.clear()
    MIN_TEMPS.clear()

    soup = get_soup_by_(INFO.generated_url, INFO.lang_code)
    return (
        f"<b>{get_many_days_title(soup)}</b>\n\n"
        f"{get_weather_info_about_many_days_from_(soup)}"
    )


def get_one_day_title(soup: BeautifulSoup) -> str:
    """For getting title from the given soup"""
    h1 = " ".join(soup.find("h1").text.strip().split()[:-1])

    swiper_slide = soup.find("div", class_="swiper-wrapper").find_all(
        "div", class_="swiper-slide"
    )[0 if INFO.about_today else 1]
    return f"{h1} {get_subtitle_from(swiper_slide).lower()}"


def get_subtitle_from(
    swiper_slide: BeautifulSoup, with_temp: Optional[bool] = False
) -> str:
    """For getting subtitle from the given swiper slide"""
    swiper_title = swiper_slide.find(
        "div", class_="thumbnail-item__title"
    ).text.strip()
    swiper_subtitle = swiper_slide.find(
        "div", class_="thumbnail-item__subtitle"
    ).text.strip()
    temp = ""
    if with_temp:
        swiper_temp = swiper_slide.find(
            "div", class_="thumbnail-item__temperature"
        )
        temp_min = swiper_temp.find(
            "div", class_="temperature-max"
        ).text.strip()
        temp_max = swiper_temp.find(
            "div", class_="temperature-min"
        ).text.strip()
        key = f"{swiper_title} ({swiper_subtitle.split()[0]})"
        MAX_TEMPS[key] = int(temp_max[:-2])  # [:-2] - remove "°C"
        MIN_TEMPS[key] = int(temp_min[:-2])  # [:-2] - remove "°C"
        temp = (
            f": {temp_max}"
            if MAX_TEMPS[key] == MIN_TEMPS[key]
            else f": {temp_min} ... {temp_max}"
        )
    return f"{swiper_title} ({swiper_subtitle}){temp}"


def get_active_swiper_slide_from(soup: BeautifulSoup) -> BeautifulSoup:
    """For getting swiper gallery from the given soup"""
    return soup.find("div", class_="swiper-gallery").find_all(
        "div", class_="swiper-slide"
    )[0 if INFO.about_today else 1]


def get_weather_info_about_day_from_(
    active_swiper_slide: BeautifulSoup,
) -> str:
    text = ""

    all_astro_li = (
        active_swiper_slide.find("div", class_="overall-day-info")
        .find("ul")
        .find_all("li")
    )
    for index, astro_li in enumerate(all_astro_li[:3]):
        astro_li_text = astro_li.text.strip().replace("\n", " — ")
        text += f"{'🌅🌆🕐'[index]} {astro_li_text}\n"
    text += "\n"

    day_emojis = ("🌃", "🌇", "🏙️", "🌆")

    for index, time_of_day in enumerate(
        active_swiper_slide.find_all("ul", class_="times-of-day__item")
    ):
        title = time_of_day.find("li", class_="title").text.strip()
        description = (
            time_of_day.find("li", class_="icon")
            .find("div", class_="item-icon")
            .get("title")
            .strip()
        )
        temperature = time_of_day.find("li", class_="temperature").text.strip()
        feels_like = (
            time_of_day.find("li", "feels_like").text.strip().split("\n\n")[-1]
        )
        text += (
            f"{day_emojis[index]} <b>{title}: {temperature} ({feels_like})</b> "
            f"{get_weather_emoji_by_(description, INFO.lang_code)}\n"
            f"{description.capitalize()}\n"
            f"{get_weather_details_by_(time_of_day)}\n"
        )
    return text


def get_weather_details_by_(time_of_day: BeautifulSoup) -> str:
    """For getting weather details on the given time of day"""
    weather_info = time_of_day.find_all("li", class_="weather-info")
    weather_details = ""
    for info in weather_info:
        icon = _get_weather_detail_icon_by_(
            info.find("div", class_="icon").get("class")[-1]
        )
        span = info.find("span")
        weather_details += (
            f"<i>{span.get('title')}:</i> {span.text.strip()} {icon}\n"
        )
    return f"<blockquote expandable>{weather_details}</blockquote>"


def get_many_days_title(soup: BeautifulSoup) -> str:
    """For getting title from the given soup"""
    title_tag = soup.find("h1")
    if title_tag is None:
        title_tag = soup.find("h2")
    title = title_tag.text.strip()

    if title.endswith(")"):
        try:
            title, detail = title.split("(")
        except ValueError:
            splitted_title = title.split("(")
            title = splitted_title[0] + "(" + splitted_title[1]
            detail = splitted_title[-1]
        title = title.strip()
        detail = f"({detail}" if detail else ""
    else:
        detail = ""

    time_title = (
        INFO.time_title.split(" ")[-1]
        if INFO.about_big_city
        else INFO.time_title
    )
    return (
        {
            "ua": " ".join(title.split()[:-1])
            + f" {time_title.lower()} {detail}",
            "ru": " ".join(title.split()[:-1])
            + f" {time_title.lower()} {detail}",
            "en": (
                f"{time_title.capitalize()} " + " ".join(title.split()[1:])
                if INFO.about_big_city
                else " ".join(title.split()[:-1])
                + f" {time_title.lower()} {detail}"
            ),
        }
        .get(INFO.lang_code)
        .strip()
    )


def get_weather_info_about_many_days_from_(
    soup: BeautifulSoup,
) -> str:
    """For getting weather info about many days from the given weather temp graph"""
    slider = soup.find("section", class_="weather-day-by-day-slider")

    thumbnails = slider.find("div", class_="swiper-thumbnails").find_all(
        "div", class_="swiper-slide"
    )
    gallery = slider.find("div", class_="swiper-gallery").find_all(
        "div", class_="swiper-slide"
    )
    text = ""

    for day in range(7 if INFO.about_week else 14):
        try:
            title = get_subtitle_from(thumbnails[day], with_temp=True)
            description = (
                gallery[day]
                .find("div", class_="swiper-extended-item__footer")
                .find("div", class_="description")
                .text.strip()
                .split(":")[-1]
                .strip()
            )
            weather_details = get_weather_details_by_(
                gallery[day].find_all("ul", class_="times-of-day__item")[2]
            )
            text += (
                f"<b>{title}</b> {get_weather_emoji_by_(description, INFO.lang_code)}\n"
                f"{description}\n"
                f"{weather_details}\n"
            )
        except (AttributeError, IndexError):
            break
    return text

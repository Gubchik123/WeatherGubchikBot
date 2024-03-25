from typing import Dict, NamedTuple, Optional

from bs4 import BeautifulSoup

from .general import get_soup_by_
from .getting_emoji import get_weather_emoji_by_
from .selected_info import SelectedInfo


INFO = SelectedInfo()

MAX_TEMPS: Dict[str, int] = {}
MIN_TEMPS: Dict[str, int] = {}


class WeatherDetail(NamedTuple):
    """For storing weather details after parsing"""

    wind: str
    rain: str
    humidity: str


class WeatherDetailTitle(WeatherDetail):
    """For storing weather detail titles by language"""


def get_information_about_weather_by_(data: dict) -> str:
    """For getting result weather message about weather"""
    INFO.set(**data)
    
    if INFO.about_one_day:
        return get_information_about_one_day()
    return get_information_about_many_days()


def get_information_about_one_day() -> str:
    """For getting result weather message about one day"""
    soup = get_soup_by_(INFO.generated_url, INFO.lang_code)
    active_swiper_slide = get_active_swiper_slide_from(soup)
    return f"{get_one_day_title(soup)}:\n{get_weather_info_about_day_from_(active_swiper_slide)}"


def get_information_about_many_days() -> str:
    MAX_TEMPS.clear()
    MIN_TEMPS.clear()

    soup = get_soup_by_(INFO.generated_url, INFO.lang_code)
    return f"{get_many_days_title(soup)}:\n{get_weather_info_about_many_days_from_(soup)}"


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
    weather_detail_title = get_weather_detail_title()
    day_emojis = ("🌃", "🌇", "🏙️", "🌆")

    text = ""

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

        text += f"""
        {day_emojis[index]} <b>{title}: {temperature}</b> {get_weather_emoji_by_(description, INFO.lang_code)}
        {description.capitalize()}

        {get_weather_details_by_(time_of_day, weather_detail_title)}
        {"_"*35}\n""".replace(
            "        ", ""
        )
    return text


def get_weather_detail_title() -> WeatherDetailTitle:
    """For getting weather detail titles by current language code"""
    return {
        "ua": WeatherDetailTitle(
            rain="Імовірність опадів", wind="Вітер", humidity="Вологість"
        ),
        "ru": WeatherDetailTitle(
            rain="Возможность осадков", wind="Ветер", humidity="Влажность"
        ),
        "en": WeatherDetailTitle(
            rain="Chance of precipitation", wind="Wind", humidity="Humidity"
        ),
    }.get(INFO.lang_code)


def get_weather_details_by_(
    time_of_day: BeautifulSoup,
    weather_detail_title: WeatherDetailTitle,
    day: Optional[int] = 0,
) -> str:
    """For getting weather details on the given time of day"""
    weather_info = time_of_day.find_all("li", class_="weather-info")
    is_full_info = day < 9
    decrement = 0 if is_full_info else 1

    weather_details = f"""{weather_detail_title.wind}: {weather_info[2 - decrement].find("span").text.strip()}  🌬
    {weather_detail_title.humidity}: {weather_info[3 - decrement].find("span").text.strip()}  💦""".replace(
        "    ", ""
    )
    if is_full_info:
        weather_details += f"\n{weather_detail_title.rain}: {weather_info[0].find('span').text.strip()}  💧"
    return weather_details


def get_many_days_title(soup: BeautifulSoup) -> str:
    """For getting title from the given soup"""
    title_tag = soup.find("h1")
    if title_tag is None:
        title_tag = soup.find("h2")
    title = title_tag.text.strip()

    if INFO.about_big_city:
        return title
    return {
        "ua": f"Прогноз погоди в {INFO.city_title} на {INFO.time_title.lower()}",
        "ru": f"Прогноз погоды в {INFO.city_title} на {INFO.time_title.lower()}",
        "en": f"{INFO.time_title.capitalize()} weather forecast in {INFO.city_title}",
    }.get(INFO.lang_code)


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
    weather_detail_title = get_weather_detail_title()
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
                gallery[day].find_all("ul", class_="times-of-day__item")[2],
                weather_detail_title,
                day,
            )
            text += f"""
            <b>{title}</b> {get_weather_emoji_by_(description, INFO.lang_code)}
            {description}

            {weather_details}
            {"_"*35}
            """.replace(
                "            ", ""
            )
        except IndexError:
            break
    return text

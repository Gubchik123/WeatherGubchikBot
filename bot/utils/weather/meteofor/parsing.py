from typing import Dict, List, Tuple, Optional

from bs4 import BeautifulSoup
from aiogram.utils.i18n import gettext as _

from ..request import get_soup_by_
from ..emoji import get_weather_emoji_by_

from .selected_info import SelectedInfo


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
    INFO.set_site_domain_by_(
        "ua" if INFO.lang_code == "ru" else INFO.lang_code
    )  # ! Workaround for valid url
    soup = get_soup_by_(INFO.generated_url, INFO.lang_code)
    return _get_weather_info_for_now_from_(soup)


def _get_weather_info_for_now_from_(soup: BeautifulSoup) -> str:
    """For getting weather message for now."""
    block = soup.find("div", class_="now")

    local_date = block.find("div", class_="now-localdate").text.strip()
    # Temperature
    temp = block.find("div", class_="now-weather").find().get("value") + "°C"
    feels_like = (
        block.find("div", class_="now-feel").text.strip()
        + " "
        + block.find("div", class_="now-feel").find().get("value")
        + "°C"
    )
    # Description
    desc = block.find("div", class_="now-desc").text.strip()
    # Details
    text = (
        f"<b>{soup.find('h1').text.strip()} - {local_date}</b>\n\n"
        f"{temp} {get_weather_emoji_by_(desc, INFO.lang_code)}\n"
        f"{feels_like}\n\n"
        f"{desc}\n\n"
    )
    for item in block.find_all("div", class_="now-info-item"):
        title = item.find("div", class_="item-title").text.strip()
        value = item.find(
            "div", class_="item-value"
        ).text.strip() or item.find("div", class_="item-value").find().get(
            "value"
        )
        text += f"<i>{title}:</i> {value}\n"
    return text


def get_information_about_one_day() -> str:
    """Returns result weather message about one day."""
    INFO.set_site_domain_by_(
        "ua" if INFO.lang_code == "ru" else INFO.lang_code
    )  # ! Workaround for valid url
    soup = get_soup_by_(INFO.generated_url, INFO.lang_code)
    times = dict(zip((0, 2, 4, 6), _get_day_period_titles()))
    return _get_weather_info_by_(soup, times.items())


def _get_day_period_titles() -> Tuple[str]:
    """Returns day period title by current language code."""
    return {
        "ua": ("🌃 Вночі", "🌇 Вранці", "🏙️ Вдень", "🌆 Увечері"),
        "ru": ("🌃 Ночью", "🌇 Утром", "🏙️ Днем", "🌆 Вечером"),
        "en": ("🌃 Night", "🌇 Morning", "🏙️ Day", "🌆 Evening"),
    }.get(INFO.lang_code)


def get_information_about_many_days() -> str:
    """Returns result weather message about many days."""
    INFO.set_site_domain_by_(
        "ua" if INFO.lang_code == "ru" else INFO.lang_code
    )  # ! Workaround for valid url

    MAX_TEMPS.clear()
    MIN_TEMPS.clear()

    soup = get_soup_by_(INFO.generated_url, INFO.lang_code)
    date_title, date_rows = _get_rows_from_div_with_class_(
        "widget-row-date", _get_widget_body_from_(soup)
    )
    return _get_weather_info_by_(soup, enumerate(date_rows))


def _get_weather_info_by_(
    soup: BeautifulSoup, times: List[Tuple[int, str]]
) -> str:
    """Returns text with weather information about one day."""
    text = f"<b>{soup.find('h1').text.strip()}</b>\n\n"

    if INFO.about_one_day:
        all_astro_divs = soup.find("div", class_="astro-times").find_all("div")
        text += (
            f"🌅 {all_astro_divs[1].text.strip()}\n"
            f"🌆 {all_astro_divs[2].text.strip()}\n"
            f"🕐 {all_astro_divs[0].text.strip()}\n"
            f"ℹ️ {soup.find('div', class_='astro-bottom').text.strip()}\n\n"
        )
    wind_symbol = _get_wind_symbol()

    widget_body = _get_widget_body_from_(soup)

    description_title, description_rows = _get_rows_from_div_with_class_(
        "widget-row-icon", widget_body
    )
    wind_title, wind_rows = _get_rows_from_div_with_class_(
        "widget-row-wind", widget_body
    )
    precipitation_title, precipitation_rows = _get_rows_from_div_with_class_(
        "widget-row-precipitation-bars", widget_body
    )
    pressure_title, pressure_rows = _get_rows_from_div_with_class_(
        "widget-row-chart-pressure", widget_body, "value"
    )
    humidity_title, humidity_rows = _get_rows_from_div_with_class_(
        "widget-row-humidity", widget_body
    )
    uv_index_title, uv_index_rows = _get_rows_from_div_with_class_(
        "widget-row-radiation", widget_body
    )
    temperature_title, temperature_rows = _get_rows_from_div_with_class_(
        "widget-row-chart-temperature-air", widget_body, "value"
    )
    feels_like_title, feels_like_rows = _get_rows_from_div_with_class_(
        "widget-row-chart-temperature-heat-index", widget_body, "value"
    )
    for row_index, time in times:
        if INFO.about_many_days:
            time = _get_pretty_day_string_from_(time)
            temp = _get_pretty_temp_string_from_(
                temperature_rows[row_index], time
            )
            pressure_max, pressure_min = _parse_maxt_mint_values_from_(
                pressure_rows[row_index]
            )
            feels_like = ""
        else:
            temp = temperature_rows[row_index].find().get("value")
            feels_like = (
                f"({feels_like_rows[row_index].find().get('value')}°C)"
            )
            pressure_max = pressure_min = (
                pressure_rows[row_index].find().get("value")
            )
        description = description_rows[row_index].get("data-tooltip")
        if not description:
            description = (
                description_rows[row_index]
                .find("div", class_="weather-icon")
                .get("data-text")
            )
        wind = wind_rows[row_index].find_all()[-1].get("value")
        humidity = humidity_rows[row_index].text.strip()
        uv_index = uv_index_rows[row_index].text.strip()
        precipitation = (
            precipitation_rows[row_index]
            .find("div", class_="item-unit")
            .text.strip()
        )
        text += (
            f"<b>{time}: {temp}°C {feels_like}</b> "
            f"{get_weather_emoji_by_(description, INFO.lang_code)}\n"
            f"{description}\n\n"
            f"<i>{wind_title}:</i> {wind} {wind_symbol} 🌬\n"
            f"<i>{precipitation_title}:</i> {precipitation} mm 💧\n"
            f"<i>{pressure_title}:</i> {pressure_max} 🌡\n"
            f"<i>{humidity_title}:</i> {humidity} % 💦\n"
            f"<i>{uv_index_title}:</i> {uv_index} 📉\n"
            f"{'_'*35}\n\n"
        )
    return text


def _get_wind_symbol() -> str:
    """Returns wind symbol by current language code."""
    return {"ua": "м/с", "en": "mps", "ru": "м/с"}.get(INFO.lang_code)


def _get_widget_body_from_(soup: BeautifulSoup) -> BeautifulSoup:
    """Returns widget body div from the given soup."""
    return soup.find("div", class_="widget-body")


def _get_rows_from_div_with_class_(
    class_: str, block: BeautifulSoup, item_class: Optional[str] = "row-item"
) -> Tuple[str, List[BeautifulSoup]]:
    """Returns rows by block class selector."""
    title = None
    detail_block = block.find("div", class_=class_)
    if p := detail_block.find("p", class_="widget-row-caption"):
        title = p.text.strip().split(",")[0]
    return (title, detail_block.find_all(class_=item_class))


def _get_pretty_day_string_from_(day_block: BeautifulSoup) -> str:
    """Returns one string from two info strings about day and date."""
    day = day_block.find("div", class_="day").text.strip()
    date = day_block.find("div", class_="date").text.strip()

    new_line = "\n"  # ! to avoid SyntaxError
    return f"{day} ({date.split(new_line)[0]})"


def _get_pretty_temp_string_from_(temp_row: BeautifulSoup, time: str) -> str:
    """Returns pretty string with temperature."""
    max_temp, min_temp = _parse_maxt_mint_values_from_(temp_row)

    MAX_TEMPS[time] = int(max_temp)
    MIN_TEMPS[time] = int(min_temp)

    return (
        f"{max_temp}"
        if MAX_TEMPS[time] == MIN_TEMPS[time]
        else f"{min_temp}°C ... {max_temp}"
    )


def _parse_maxt_mint_values_from_(row: BeautifulSoup) -> str:
    """Returns pretty string with max and min temperature."""
    max_temp = int(row.find("div", class_="maxt").find().get("value"))
    min_temp = int(row.find("div", class_="mint").find().get("value"))
    return max_temp, min_temp

from typing import Tuple, Union
from collections import OrderedDict

import aiohttp
from emoji import emojize
from bs4 import BeautifulSoup

from .parsing import INFO


async def get_searched_data_with_(
    user_input: str, lang_code: str
) -> Tuple[Union[str, dict], bool]:
    """Returns searched list of cities, or exact city."""
    INFO.set_site_domain_by_(lang_code)
    cities = OrderedDict()

    text = await _fetch_search_page_with_(user_input)

    for catalog_item in _parse_catalog_items_from_(text, lang_code):
        if len(cities) == 20:
            break
        if _is_terrorist_in_(catalog_item):
            continue
        city_url = _extract_city_data(catalog_item, user_input, cities)
        if city_url:
            return city_url, True
    return cities, False


async def _fetch_search_page_with_(user_input: str) -> str:
    """Returns response text from search page by the given user input text."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{INFO.site_domain}/search/{user_input}/"
        ) as response:
            return await response.text()


def _parse_catalog_items_from_(text: str, lang_code: str) -> BeautifulSoup:
    """Returns parsed catalog items
    from the given response text and by the given language code."""
    soup = BeautifulSoup(text, "lxml")
    catalog_lists = soup.find_all("div", class_="catalog-list")
    return catalog_lists[-1].find_all("div", class_="catalog-group-items")


def _is_terrorist_in_(catalog_item: BeautifulSoup) -> bool:
    """Checks if the given catalog item is terrorist country."""
    for terrorist in ("Росія", "Россия", "Russia"):
        if terrorist in catalog_item.find_all("a")[-1].text:
            return True
    return False


def _extract_city_data(
    catalog_item: BeautifulSoup, user_input: str, cities: OrderedDict
) -> Union[str, None]:
    """Extracts city title and url from the given catalog item.
    Fills the given cities ordered dict or return exact city url."""
    city_link = catalog_item.find("a")
    city_title = city_link.text.strip().split("(")[0].strip().lower()
    city_url = city_link.get("href")

    if city_title == user_input:
        return city_url

    country_flag_emoji = _get_country_flag_emoji_from_(catalog_item)
    city_key = f"{country_flag_emoji} {city_title}".strip()

    if city_key not in cities:
        cities[city_key] = city_url
    return None


def _get_country_flag_emoji_from_(catalog_item: BeautifulSoup) -> str:
    """Returns country flag emoji or white (default) flag
    from breadcrumbs of the given catalog item."""
    country_link: BeautifulSoup = catalog_item.find_all("a")[-1]
    country_url = country_link.get("href")
    country_title = (
        country_url.split("/")[-2].title()
        if country_url.endswith("/")
        else country_url.split("/")[-1].title()
    )
    country_flag_emoji_name = f":{country_title}:"
    country_flag_emoji = emojize(country_flag_emoji_name)

    return (
        emojize(":white_flag:")
        if country_flag_emoji_name == country_flag_emoji
        else country_flag_emoji
    )

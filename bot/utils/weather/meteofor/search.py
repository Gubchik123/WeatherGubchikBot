from typing import Tuple, Union
from collections import OrderedDict

import aiohttp
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
    return catalog_lists[-1].find_all(
        "div", class_=_get_catalog_item_class_by_(lang_code)
    )


def _get_catalog_item_class_by_(lang_code: str) -> str:
    """Returns class name of the catalog item by the given language code."""
    return {
        "en": "catalog-group-items",
        "ua": "catalog-item-link",
        "ru": "catalog-item-link",
    }.get(lang_code)


def _is_terrorist_in_(catalog_item: BeautifulSoup) -> bool:
    """Checks if the given catalog item is terrorist country."""
    for terrorist in ("Росія", "Россия", "Russia"):
        if terrorist in catalog_item.text:
            return True
    return False


def _extract_city_data(
    catalog_item: BeautifulSoup, user_input: str, cities: OrderedDict
) -> Union[str, None]:
    """Extracts city title and url from the given catalog item.
    Fills the given cities ordered dict or return exact city url."""
    link = catalog_item.find("a")
    # TODO: Add country flag emoji
    city_title = link.text.strip().split("(")[0].strip().lower()
    city_url = link.get("href")

    if city_title == user_input:
        return city_url

    if city_title not in cities:
        cities[city_title] = city_url
    return None

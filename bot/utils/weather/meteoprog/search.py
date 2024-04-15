import aiohttp
from collections import OrderedDict
from typing import NamedTuple, Tuple, Union

from emoji import emojize
from user_agent import generate_user_agent

from data.emojis import COUNTRIES_FLAG_EMOJIS


class City(NamedTuple):
    """Named tuple to represent city (json data item)."""

    name: str
    country: str
    region: str
    url: str
    en_name: str
    site_number: str
    empty_string: str


async def get_searched_data_with_(
    user_input: str, lang_code: str
) -> Tuple[Union[str, dict], bool]:
    """Returns searched dict of countries or cities, or exact city."""
    response_json = await _get_response_json_by_(user_input, lang_code)
    cities = OrderedDict()

    for city in [City(*data) for data in response_json["data"]]:
        if _is_terrorist_(city):
            continue
        if city.name.lower() == user_input:
            return city.en_name, True
        country_flag_emoji = _get_country_flag_emoji_by_(
            city.country, lang_code
        )
        cities[f"{country_flag_emoji} {city.name}"] = city.url
    return cities, False


async def _get_response_json_by_(user_input: str, lang_code: str) -> dict:
    """Returns response json from the weather provider site."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://www.meteoprog.com/{lang_code}/search/json?q={user_input}",
            headers={"user-agent": generate_user_agent().strip()},
            cookies={"cookie": f"needed_thing=''; default_lang={lang_code};"},
        ) as resp:
            return await resp.json()


def _is_terrorist_(city: City) -> bool:
    """Checks if the data item is terrorist country."""
    return city.country in ("Росія", "Россия", "Russia")


def _get_country_flag_emoji_by_(country_name: str, lang_code: str) -> str:
    """Returns country flag emoji or white (default) flag
    by the given country name and language code."""
    emoji_name = (
        f":{country_name.replace(' ', '_')}:"
        if lang_code == "en"
        else COUNTRIES_FLAG_EMOJIS.get(country_name, ":white_flag:")
    )
    emoji = emojize(emoji_name)

    return emojize(":white_flag:") if emoji_name == emoji else emoji

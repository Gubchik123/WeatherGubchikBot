import aiohttp
from typing import Tuple, Union
from collections import OrderedDict

from user_agent import generate_user_agent


async def get_searched_data_with_(
    user_input: str, lang_code: str
) -> Tuple[Union[str, dict], bool]:
    """For getting searched dict of countries or cities, or exact city."""
    response_json = await _get_response_json_by_(user_input, lang_code)
    result_data = response_json["data"]
    if result_data and (
        len(result_data) == 1 or result_data[0][0].lower() == user_input
    ):
        return result_data[0][4], True
    return _get_filtered_(result_data), False


async def _get_response_json_by_(user_input: str, lang_code: str) -> dict:
    """For getting response json from the weather provider site."""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://www.meteoprog.com/{lang_code}/search/json?q={user_input}",
            headers={"user-agent": generate_user_agent().strip()},
            cookies={"cookie": f"needed_thing=''; default_lang={lang_code};"},
        ) as resp:
            return await resp.json()


def _get_filtered_(result_data: list) -> OrderedDict:
    """For getting filtered ordered dict of countries or cities"""
    return OrderedDict(  # TODO: Add country flag emoji
        (data[0].lower() if data[2] else "", data[4])
        for data in result_data
        if data[1] not in ("Росія", "Россия", "Russia")
    )

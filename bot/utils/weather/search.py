from typing import Tuple, Union

import requests
from user_agent import generate_user_agent


def _get_response_json_by_(user_input: str, lang_code: str) -> dict:
    """For getting response json from the weather provider site."""
    return requests.get(
        f"https://www.meteoprog.com/{lang_code}/search/json?q={user_input}",
        headers={"user-agent": generate_user_agent().strip()},
        cookies={"cookie": f"needed_thing=''; default_lang={lang_code};"},
    ).json()


def _get_filtered_(result_data: list) -> list:
    """For getting filtered list of countries or cities"""
    return {
        data[0].lower() + f" ({data[2].lower()})" if data[2] else "": data[4]
        for data in result_data
        if data[1] not in ("Росія", "Россия", "Russia")
    }


def get_searched_data_with_(
    user_input: str, lang_code: str
) -> Tuple[Union[str, list], bool]:
    """For getting searched list of countries or cities, or exact city."""
    result_data = _get_response_json_by_(user_input, lang_code)["data"]
    is_match_100 = result_data and result_data[0][0].lower() == user_input

    if is_match_100:
        return result_data[0][4], is_match_100

    return _get_filtered_(result_data), is_match_100
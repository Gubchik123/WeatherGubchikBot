from typing import Tuple, Union

import requests
from user_agent import generate_user_agent

from constants import INFO, TEXT


def _get_response_json_by_(user_input: str) -> dict:
    """For getting response json from meteoprog.ua"""
    lang_code = TEXT().lang_code
    return requests.get(
        f"https://www.meteoprog.ua/{lang_code}/search/json?q={user_input}",
        headers={"user-agent": generate_user_agent().strip()},
        cookies={"cookie": f"needed_thing=''; default_lang={lang_code};"},
    ).json()


def _get_filtered_(result_data: list) -> list:
    """For getting filtered list of countries or cities"""
    return {
        f"{data[0].lower()} ({data[2].lower()})": data[4]
        for data in result_data
        if data[1] not in ("Росія", "Россия", "Russia")
    }


def get_searched_data_with_(user_input: str) -> Tuple[Union[str, list], bool]:
    """For getting searched list of countries or cities, or exact city."""
    result_data = _get_response_json_by_(user_input)["data"]
    is_match_100 = result_data and result_data[0][0].lower() == user_input

    if is_match_100:
        return result_data[0][4], is_match_100

    return _get_filtered_(result_data), is_match_100

import requests
from bs4 import BeautifulSoup
from aiogram.utils.i18n import gettext as _
from user_agent import generate_user_agent


class WeatherProviderServerError(Exception):
    """Exception for server error from the weather provider."""


class InvalidResponse(Exception):
    """Exception for invalid response from GET request to the site."""


def get_soup_by_(url: str, lang_code: str) -> tuple:
    """For getting BeautifulSoup object by url"""
    if lang_code != "ua":
        url = url.replace("/ua/", f"/{lang_code}/")

    response = _get_response_from_(url, lang_code)
    return BeautifulSoup(response.text, "lxml")


def _get_response_from_(url: str, lang_code: str) -> tuple:
    """For sending GET request to url and getting response"""
    headers = {"user-agent": generate_user_agent().strip()}
    cookies = {"cookie": f"needed_thing=''; default_lang={lang_code};"}

    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code == 410:
        url = (
            url.replace("review", "weather")
            if "review" in url
            else "/".join(url.split("/")[:-1])
        )  # set url for one day
        response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code >= 500:
        raise WeatherProviderServerError(
            f"Server error from the weather provider ({response.status_code}):"
            f"\n{url=}\n{response.text=}\n{response.json()}"
        )
    elif not response.ok:
        raise InvalidResponse(
            f"Not OK server response from the site ({response.status_code}):"
            f"\n{url=}\n{response.text=}\n{response.json()}"
        )
    return response

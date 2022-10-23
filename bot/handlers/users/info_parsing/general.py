import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiogram import types

from constants import TEXT


def get_soup_by_(url: str):
    global TEXT

    lang_code = TEXT().lang_code
    lang_code = lang_code.replace("uk", "ua")

    headers = {'user-agent': UserAgent().random}
    cookie = {"cookie": f"needed_thing=''; default_lang={lang_code};"}

    if lang_code != "uk":
        url = url.replace("/ua/", f"/{lang_code}/")

    response = requests.get(url, headers=headers, cookies=cookie)
    return BeautifulSoup(response.text, 'lxml')


def get_block_and_title_from(soup: BeautifulSoup):
    block = soup.find("div", class_="page-columns-wrapper")
    title = block.find("h1").text.strip()

    return block, title


async def send_message_to_user_about_error(message: types.Message, error):
    global TEXT
    await message.answer(TEXT().error_message())
    print(f"Exception: {error}")

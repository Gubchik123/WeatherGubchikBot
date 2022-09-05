import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiogram import types

from constants import TEXT


def get_soup_by(url: str):
    response = requests.get(url, headers={'user-agent': UserAgent().random})
    return BeautifulSoup(response.text, 'lxml')


def get_block_and_title_from(soup: BeautifulSoup):
    block = soup.find("div", class_="page-columns-wrapper")
    title = block.find("h1").text.strip()

    return block, title


async def send_message_to_user_about_error(message: types.Message, error):
    global TEXT
    await message.answer(TEXT.error_message())
    print(f"Exception: {error}")

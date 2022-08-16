import os
import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiogram import types

from constants import BASE_DIR


def get_soup_by(url: str):
    response = requests.get(url, headers={'user-agent': UserAgent().random})
    return BeautifulSoup(response.text, 'lxml')


def get_block_and_title_from(soup: BeautifulSoup):
    block = soup.find("div", class_="page-columns-wrapper")
    title = block.find("h1").text.strip()

    return block, title


async def print_error(message: types.Message, error):
    await message.answer("Виникла помилка! (Error)\n"
                         "Спробуйте повторити спробу")
    print(error)

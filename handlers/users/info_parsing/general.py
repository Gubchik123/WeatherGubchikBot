import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiogram import types


def get_soup_by(url: str):
    try:
        agent = UserAgent().random
    except IndexError:
        agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

    response = requests.get(url, headers={'user-agent': agent})
    return BeautifulSoup(response.text, 'lxml')


def get_block_and_title_from(soup: BeautifulSoup):
    block = soup.find("div", class_="page-columns-wrapper")
    title = block.find("h1").text.strip()

    return block, title


async def print_error(message: types.Message, error):
    await message.answer("Виникла помилка! (Error)\n"
                         "Спробуйте повторити спробу")
    print(error)

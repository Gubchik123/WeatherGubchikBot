from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import MY_DB
from keyboard import make_reply_keyboard_markup, make_button


@DP.message_handler(Text("управління розсилкою", ignore_case=True))
async def managment(message: types.Message):
    id = message.from_user.id
    data = MY_DB.get_information_about_user_with_(id)

    mute = data["mute"]
    city = data["city"]
    time = data["time"]
    time_int = data["time_int"]

    mute_btn_text = "режим оповіщення" if mute else "беззвучний режим"

    markup = make_reply_keyboard_markup(width=2)
    markup.add(make_button(f"Увімкнути {mute_btn_text}"),
               make_button("Змінити час розсилки"))
    markup.add(make_button("Змінити місто"),
               make_button("Змінити період прогнозу"))
    markup.add(make_button("Вимкнути розсилку"))
    markup.add(make_button("← Повернутися у головне меню"))

    await message.answer("Ви в меню управління розсилкою\n"
                         "Деталі вашої розсилки:\n\n"
                        f"Час: {time_int}:00\n"
                         "Кожен день\n"
                        f"Режим: {'Беззвучний' if mute else 'Оповіщення'}\n\n"
                        f"Місто: {city}\n"
                        f"Період прогнозу: {time}")
    await message.answer("Що ви хочете зробити?", reply_markup=markup)
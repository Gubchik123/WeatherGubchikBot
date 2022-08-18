from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import MY_DB
from keyboard import make_reply_keyboard_markup, make_button


@DP.message_handler(Text("управління розсилкою", ignore_case=True))
async def managment(message: types.Message):
    id = message.from_user.id
    mute, city = MY_DB.get_information_about_user_with_(id)

    mute_btn_text = "режим оповіщення" if mute else "беззвучний режим"

    markup = make_reply_keyboard_markup(width=2)
    markup.add(make_button(f"Увімкнути {mute_btn_text}"),
               make_button("Змінити місто"))
    markup.add(make_button("Вимкнути розсилку"))
    markup.add(make_button("← Повернутися у головне меню"))

    await message.answer("Ви в меню управління розсилкою\n\n"
                         "Деталі вашої розсилки:\n"
                         "Час: 09:00\n"
                         "Кожен день\n"
                         f"Режим: {'Беззвучний' if mute else 'Оповіщення'}\n\n"
                         f"Місто: {city}\n"
                         "Період прогнозу: сьогодні")
    await message.answer("Що ви хочете зробити?", reply_markup=markup)


@DP.message_handler(Text("увімкнути режим оповіщення", ignore_case=True))
async def turn_off_mute_mode_for_mailing(message: types.Message):
    id = message.from_user.id
    MY_DB.update_user_with(id, what_update="mute", new_item=False)

    await managment(message)


@DP.message_handler(Text("увімкнути беззвучний режим", ignore_case=True))
async def turn_on_mute_mode_for_mailing(message: types.Message):
    id = message.from_user.id
    MY_DB.update_user_with(id, what_update="mute", new_item=True)

    await managment(message)

from aiogram import types

from constants import MY_DB
from keyboard import make_reply_keyboard_markup, make_button


async def menu(message: types.Message):
    chat_IDs = MY_DB.chat_IDs
    mailing_action = "Вимкнути" if message.from_user.id in chat_IDs else "Увімкнути"

    markup = make_reply_keyboard_markup(width=2)
    markup.add(make_button("Переглянути прогноз погоди"),
               make_button("Переглянути фазу місяця"))
    markup.add(make_button(f"{mailing_action} розсилку"))
    markup.add(make_button("Закінчити спілкування"))

    await message.answer("Виберіть подальші дії", reply_markup=markup)

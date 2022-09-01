from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import MY_DB, INFO
from keyboard import make_keyboard_for_country_choosing, make_button


@DP.message_handler(Text("← повернутися у головне меню", ignore_case=True))
async def menu(message: types.Message):
    global INFO

    chat_IDs: list = MY_DB.chat_IDs
    mailing_btn_text = "Управління розсилкою" \
        if message.from_user.id in chat_IDs \
        else "Увімкнути розсилку"

    INFO.goal = "normal"

    markup = make_keyboard_for_country_choosing()
    markup.add(make_button(mailing_btn_text))
    markup.add(make_button("Закінчити спілкування"))

    await message.answer("Ви в головному меню\n"
                         "Виберіть подальші дії", reply_markup=markup)

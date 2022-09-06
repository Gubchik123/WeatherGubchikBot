from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import MY_DB, INFO, TEXT
from keyboard import make_keyboard_for_country_choosing, make_button

variants: tuple = (
    "← повернутися у головне меню", 
    "← вернуться в главное меню",
    "← return to the main menu"
)


@DP.message_handler(Text(variants[0], ignore_case=True))
@DP.message_handler(Text(variants[1], ignore_case=True))
@DP.message_handler(Text(variants[2], ignore_case=True))
async def menu(message: types.Message):
    global INFO, TEXT

    if message.text.lower() in variants:
        TEXT.change_on_detected_language_from(message.text.lower())

    chat_IDs: list = MY_DB.chat_IDs
    mailing_btn_text = TEXT.menu_btn_mailing_managment() \
        if message.from_user.id in chat_IDs \
        else TEXT.menu_btn_turn_on_mailing()

    INFO.goal = "normal"

    markup = make_keyboard_for_country_choosing()
    markup.add(make_button(mailing_btn_text))
    markup.add(make_button(TEXT.menu_btn_goodbye()))

    await message.answer(TEXT.menu_message(), reply_markup=markup)

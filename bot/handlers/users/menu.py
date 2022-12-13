from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import MY_DB, INFO, TEXT
from keyboard import make_keyboard_for_country_choosing, make_button


variants: tuple = (
    "← повернутися у головне меню",
    "← вернуться в главное меню",
    "← return to the main menu",
)


def _check_language_from_(text: types.Message, *, uk_word: str, ru_word: str) -> None:
    """For comparing current language with user message and changing if needed"""
    global TEXT

    lang_code = "uk" if uk_word in text else ("ru" if ru_word in text else "en")
    TEXT.check_language_by_(lang_code)


@DP.message_handler(Text(variants[0], ignore_case=True))
@DP.message_handler(Text(variants[1], ignore_case=True))
@DP.message_handler(Text(variants[2], ignore_case=True))
async def menu(message: types.Message):
    """For getting the bot menu"""
    global INFO, TEXT

    user_message = message.text.lower()

    if user_message in variants:
        _check_language_from_(user_message, uk_word="головне", ru_word="главное")

    mailing_btn_text = (
        TEXT().menu_btn_mailing_management()
        if message.from_user.id in MY_DB.chat_IDs
        else TEXT().menu_btn_turn_on_mailing()
    )

    INFO.goal = "normal"

    markup = make_keyboard_for_country_choosing()
    markup.add(make_button(mailing_btn_text))
    markup.add(make_button(TEXT().menu_btn_goodbye()))

    await message.answer(TEXT().menu_message(), reply_markup=markup)

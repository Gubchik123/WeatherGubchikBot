from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import MY_DB, TEXT
from keyboard import make_keyboard, make_button

from ..menu import _check_language_from_


variants = ("управління розсилкою", "управление рассылкой", "mailing management")


@DP.message_handler(Text(variants[0], ignore_case=True))
@DP.message_handler(Text(variants[1], ignore_case=True))
@DP.message_handler(Text(variants[2], ignore_case=True))
async def management(message: types.Message):
    global TEXT
    user_text = message.text.lower()

    if user_text in variants:
        _check_language_from_(user_text, uk_word="управління", ru_word="управление")

    data = MY_DB.get_information_about_user_with_(message.from_user.id)

    mute = data["mute"]
    mute_btn_text = TEXT().unmute_mode_btn() if mute else TEXT().mute_mode_btn()

    markup = make_keyboard(width=2)
    markup.add(
        make_button(mute_btn_text),
        make_button(TEXT().change_mailing_time_btn()),
        make_button(TEXT().change_mailing_city_btn()),
        make_button(TEXT().change_mailing_period_btn()),
        make_button(TEXT().turn_off_mailing_btn()),
    )
    markup.add(make_button(TEXT().back_to_menu_btn()))

    await message.answer(
        TEXT().mailing_info_message(data["time_int"], mute, data["time"], data["city"])
    )
    await message.answer(
        TEXT().what_do_you_want_to_do_with_mailing_message(), reply_markup=markup
    )

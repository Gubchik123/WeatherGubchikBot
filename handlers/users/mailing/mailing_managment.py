from aiogram import types
from aiogram.dispatcher.filters import Text
from googletrans import Translator

from bot_info import DP
from constants import MY_DB, TEXT
from keyboard import make_keyboard, make_button

variants = (
    "управління розсилкою",
    "управление рассылкой",
    "mailing management"
)


@DP.message_handler(Text(variants[0], ignore_case=True))
@DP.message_handler(Text(variants[1], ignore_case=True))
@DP.message_handler(Text(variants[2], ignore_case=True))
async def managment(message: types.Message):
    global TEXT

    if message.text.lower() in variants:
        TEXT.change_on_detected_language_from(message.text)

    id = message.from_user.id
    data = MY_DB.get_information_about_user_with_(id)

    mute = data["mute"]
    city = data["city"]
    time = data["time"]
    time_int = data["time_int"]

    mute_btn_text = TEXT.unmute_mode_btn() if mute else TEXT.mute_mode_btn()

    markup = make_keyboard(width=2)
    markup.add(make_button(mute_btn_text),
               make_button(TEXT.change_mailing_time_btn()))
    markup.add(make_button(TEXT.change_mailing_city_btn()),
               make_button(TEXT.change_mailing_period_btn()))
    markup.add(make_button(TEXT.turn_off_mailing_btn()))
    markup.add(make_button(TEXT.back_to_menu_btn()))

    mailing_info_message = f"""
    Ви в меню управління розсилкою
    Деталі вашої розсилки:

    Щодня о {time_int}:00
    Режим: {'Беззвучний' if mute else 'Оповіщення'}

    Період прогнозу: {time}
    Місто / населений пункт: {city}
    """.replace("    ", '')

    if TEXT.lang_code != "uk":
        mailing_info_message = Translator().translate(mailing_info_message,
                                                      dest=TEXT.lang_code).text

    await message.answer(mailing_info_message)
    await message.answer(TEXT.what_do_you_want_to_do_with_mailing_message(),
                         reply_markup=markup)

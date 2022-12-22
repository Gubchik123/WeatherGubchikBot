from aiogram import types
from aiogram.dispatcher.filters import Text

from bot_info import DP
from constants import MY_DB, TEXT
from keyboard import make_keyboard, make_button

from ..menu import _check_language_from_


variants = ("управління розсилкою", "управление рассылкой", "mailing management")


def _get_mailing_menu_keyboard_with_(mute: bool) -> types.ReplyKeyboardMarkup:
    """For getting mailing menu keyboard"""
    markup = make_keyboard(width=2)
    markup.add(
        make_button(TEXT().unmute_mode_btn() if mute else TEXT().mute_mode_btn()),
        make_button(TEXT().change_mailing_time_btn()),
        make_button(TEXT().change_mailing_city_btn()),
        make_button(TEXT().change_mailing_period_btn()),
        make_button(TEXT().turn_off_mailing_btn()),
    )
    markup.add(make_button(TEXT().back_to_menu_btn()))
    return markup


@DP.message_handler(Text(variants[0], ignore_case=True))
@DP.message_handler(Text(variants[1], ignore_case=True))
@DP.message_handler(Text(variants[2], ignore_case=True))
async def mailing_menu(message: types.Message) -> None:
    """The handler for getting the mailing menu"""
    global TEXT
    user_text = message.text.lower()

    if user_text in variants:
        _check_language_from_(user_text, uk_word="управління", ru_word="управление")

    user = MY_DB.get_user_with_(chat_id=message.from_user.id)

    await message.answer(
        TEXT().mailing_info_message(
            user.time_int, user.mute, user.time_title, user.city_title
        )
    )
    await message.answer(
        TEXT().what_do_you_want_to_do_with_mailing_message(),
        reply_markup=_get_mailing_menu_keyboard_with_(user.mute),
    )

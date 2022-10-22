from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_info import DP
from states import Mailing
from constants import MY_DB, INFO, TEXT
from utils.class_User import TelegramUser
from keyboard import make_keyboard_for_country_choosing

from ..menu import menu
from ..mailing_info import ask_about_mailing_mute_mode, select_mailing_time

from .mailing_managment import managment
from .mailing_action import turn_on_mailing
from .general import cancel_action, there_is_no_such_type_of_answer_try_again

MUTE = None
REASON = ""


@DP.message_handler(state=Mailing.turn_on)
async def checking_answer_about_turning_on_mailing(message: types.Message, state: FSMContext):
    global INFO, TEXT
    
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT().yes_btn().lower():
        await state.finish()

        INFO.goal = "mailing"
        
        markup = make_keyboard_for_country_choosing()
        await message.answer(TEXT().choose_mailing_country_question_message(),
                             reply_markup=markup)
    elif user_answer == TEXT().no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(turn_on_mailing, message)


@DP.message_handler(state=Mailing.mute_mode)
async def checking_answer_about_mailing_mute_mode(message: types.Message):
    global MUTE, TEXT

    user_answer = message.text.lower()

    if user_answer not in (TEXT().yes_btn().lower(), TEXT().no_btn().lower()):
        await there_is_no_such_type_of_answer_try_again(ask_about_mailing_mute_mode, message)

    MUTE = True if user_answer == TEXT().yes_btn().lower() else False
    await select_mailing_time(message, "mailing")


@DP.message_handler(state=Mailing.time)
async def check_selected_mailing_time(message: types.Message, state: FSMContext):
    global INFO, TEXT

    user_text = message.text.lower()
    await state.finish()

    if user_text in ["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]:
        time_int = int(user_text.split(':')[0])

        if INFO.goal == "mailing":
            INFO.lang = TEXT().lang_code
            await confirm_mailing_for_user(
                message,
                time=time_int
            )
        else:
            id = message.from_user.id

            MY_DB.update_user_with(
                id, what_update="time_int", new_item=time_int)
            await managment(message)
    else:
        await there_is_no_such_type_of_answer_try_again(select_mailing_time, message)


async def confirm_mailing_for_user(message: types.Message, time: int):
    global TEXT

    MY_DB.add(
        user=TelegramUser(message, mute_mode=MUTE, time=time),
        info=INFO
    )

    await message.answer(TEXT().successfully_turn_on_mailing_message())
    await menu(message)

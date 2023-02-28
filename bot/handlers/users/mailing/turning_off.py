from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_info import DP
from states import Mailing
from constants import MY_DB, TEXT

from .action import turn_off_mailing
from .general import cancel_action, there_is_no_such_type_of_answer_try_again

from ..menu import menu
from ..weather.general import send_message_to_user_about_error


@DP.message_handler(state=Mailing.turn_off)
async def checking_answer_about_turning_off_mailing(
    message: types.Message, state: FSMContext
) -> None:
    """For checking user answer about turning off mailing"""
    user_answer = message.text.lower()
    await state.finish()

    if user_answer == TEXT().yes_btn().lower():
        await withdraw_mailing_for_user(message, state)
    elif user_answer == TEXT().no_btn().lower():
        await cancel_action(message)
    else:
        await there_is_no_such_type_of_answer_try_again(
            turn_off_mailing, message
        )


async def withdraw_mailing_for_user(
    message: types.Message, state: FSMContext
) -> None:
    """For withdrawing mailing and deleting user from db"""
    try:
        MY_DB.delete_user_with_(message.from_user.id)
        await message.answer(TEXT().successfully_turn_off_mailing_message())
    except Exception as e:
        await send_message_to_user_about_error(
            message, str(e), error_place=" during deleting user from mailing"
        )
    finally:
        await state.finish()
        await menu(message)

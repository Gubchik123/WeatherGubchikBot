from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery
from sqlalchemy.exc import IntegrityError

from utils.decorators import before_handler_clear_state
from utils.db.crud.user import create_user_by_, update_user_with_
from keyboards.inline.profile.language import get_language_inline_keyboard

from ..menu import handle_menu


router = Router()


@router.message(CommandStart())
@before_handler_clear_state
async def handle_start_command(message: Message, *args):
    """Handles the /start command.
    Creates a new user in the database if it does not exist."""
    try:
        create_user_by_(message.from_user)
        await message.answer(
            "UA - Оберіть мову\nEN - Choose language\nRU - Выберите язык\n",
            reply_markup=get_language_inline_keyboard(action="start"),
        )
    except IntegrityError:  # psycopg2.errors.UniqueViolation
        await _greet_user(message, message.from_user.full_name)


@router.callback_query(F.data.startswith("btn_start_lang"))
async def handle_choose_start_language(callback_query: CallbackQuery):
    """Handles the language selection on start."""
    update_user_with_(
        callback_query.from_user.id, locale=callback_query.data.split("_")[-1]
    )
    await callback_query.message.delete()
    await _greet_user(
        callback_query.message, callback_query.from_user.full_name
    )


async def _greet_user(message: Message, user_full_name: str):
    """Sends a greeting message to the user."""
    await message.answer_sticker(
        "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    )
    await message.answer(
        _(
            "Hello, {name}!\n"
            "I am the one who will help you find out information about the weather in cities around the world."
        ).format(name=user_full_name)
    )
    await handle_menu(message)

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery

from keyboards.inline.language import get_language_inline_keyboard
from utils.db.crud.user import create_user_by_, change_user_locale_by_


router = Router()


@router.message(CommandStart())
async def handle_start_command(message: Message):
    create_user_by_(message.from_user)
    await message.answer(
        "UA - Оберіть мову\nEN - Choose language\nRU - Выберите язык\n",
        reply_markup=get_language_inline_keyboard(action="start"),
    )


@router.callback_query(F.data.startswith("btn_start_lang"))
async def handle_choose_language(callback_query: CallbackQuery):
    locale = callback_query.data.split("_")[-1]

    change_user_locale_by_(callback_query.from_user.id, locale)

    await callback_query.message.delete()
    await callback_query.message.answer_sticker(
        "CAACAgIAAxkBAAIB0mLG7bJvk_WJoRbWYZ6R7sGTQ9ANAAICBAAC0lqIAQIoJ02u67UxKQQ"
    )
    await callback_query.message.answer(
        _(
            "Hello, {name}!\n"
            "I am the one who will help you find out information about the weather in cities around the world."
        ).format(name=callback_query.from_user.full_name)
    )

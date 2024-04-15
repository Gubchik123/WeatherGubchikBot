from aiogram import Router
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.exceptions import TelegramBadRequest

from filters.is_private_chat_type import IsPrivateChatType


router = Router()


@router.message(IsPrivateChatType())
async def handle_all_other_messages(message: Message):
    """Handles all other messages."""
    try:
        await message.answer(
            _(
                "I don't understand you :(\n"
                "I advise you to use the buttons or commands for the intended result."
            )
        )
    except TelegramBadRequest:
        pass

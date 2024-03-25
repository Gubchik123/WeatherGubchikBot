from aiogram import Router
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _


router = Router()


@router.message()
async def handle_all_other_messages(message: Message):
    """Handles all other messages."""
    await message.answer(
        _(
            "I don't understand you :(\n"
            "I advise you to use the buttons or commands for the intended result."
        )
    )

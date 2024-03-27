from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..mailing import handle_mailing_menu


router = Router()


@router.message(Command("mailing"))
async def handle_mailing_command(message: Message):
    """Handles the /mailing command."""
    await handle_mailing_menu(message)

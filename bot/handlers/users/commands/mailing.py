from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import before_handler_clear_state

from ..mailing import handle_mailing_menu


router = Router()


@router.message(Command("mailing"))
@before_handler_clear_state
async def handle_mailing_command(message: Message, *args):
    """Handles the /mailing command."""
    await handle_mailing_menu(message)

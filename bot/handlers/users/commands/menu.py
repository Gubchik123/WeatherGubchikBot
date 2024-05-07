from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import before_handler_clear_state

from ..menu import handle_menu


router = Router()


@router.message(Command("menu"))
@before_handler_clear_state
async def handle_menu_command(message: Message, *args) -> None:
    """Handles the /menu command."""
    await handle_menu(message)

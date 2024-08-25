from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import before_handler_clear_state
from filters.is_private_chat_type import IsPrivateChatType

from ..menu import handle_menu


router = Router()


@router.message(IsPrivateChatType(), Command("menu"))
@before_handler_clear_state
async def handle_menu_command(message: Message, **kwargs) -> None:
    """Handles the /menu command."""
    await handle_menu(message)

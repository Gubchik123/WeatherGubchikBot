from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import before_handler_clear_state
from filters.is_private_chat_type import IsPrivateChatType

from ..mailing import handle_mailing_menu


router = Router()


@router.message(IsPrivateChatType(), Command("mailing"))
@before_handler_clear_state
async def handle_mailing_command(message: Message, *args):
    """Handles the /mailing command."""
    await handle_mailing_menu(message)

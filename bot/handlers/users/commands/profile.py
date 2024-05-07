from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import before_handler_clear_state
from filters.is_private_chat_type import IsPrivateChatType

from ..profile import handle_profile


router = Router()


@router.message(IsPrivateChatType(), Command("profile"))
@before_handler_clear_state
async def handle_profile_command(message: Message, *args):
    """Handles the /profile command."""
    await handle_profile(message)

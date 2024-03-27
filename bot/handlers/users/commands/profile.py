from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import before_command_clear_state

from ..profile import handle_profile


router = Router()


@router.message(Command("profile"))
@before_command_clear_state
async def handle_profile_command(message: Message):
    """Handles the /profile command."""
    await handle_profile(message)

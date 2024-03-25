from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..profile import handle_profile


router = Router()


@router.message(Command(commands=["profile"]))
async def handle_profile_command(message: Message):
    """Handles the /profile command."""
    await handle_profile(message)

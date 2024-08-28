from typing import List

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin
from utils.db.crud.user import get_all_channels, get_all_channels_count

from .users import _send_list_of_users


router = Router()


@router.message(IsAdmin(), Command("channels"))
async def handle_all_channels_command(message: Message) -> None:
    """Handles the /channels command."""
    await _send_list_of_users(message, get_all_channels())


@router.message(IsAdmin(), Command("channels_count"))
async def handle_all_channels_count_command(message: Message) -> None:
    """Handles the /channels_count command."""
    await message.answer(f"👥 {get_all_channels_count()}")

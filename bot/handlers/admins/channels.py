from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin
from utils.db.models import User
from utils.db.crud.user import get_users, get_users_count

from .users import _send_list_of_users


router = Router()


@router.message(IsAdmin(), Command("channels"))
async def handle_all_channels_command(message: Message) -> None:
    """Handles the /channels command."""
    await _send_list_of_users(message, get_users(condition=User.chat_id < 0))


@router.message(IsAdmin(), Command("channels_count"))
async def handle_all_channels_count_command(message: Message) -> None:
    """Handles the /channels_count command."""
    await message.answer(f"👥 {get_users_count(condition=User.chat_id < 0)}")

from typing import List

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import command_argument_required
from filters.is_admin import IsAdmin
from utils.db.models import User
from utils.db.crud.user import (
    get_user_by_,
    get_all_users,
    get_all_users_count,
    get_all_mailing_users,
    get_all_mailing_users_count,
)


router = Router()


@router.message(IsAdmin(), Command("users_count"))
async def handle_all_users_count_command(message: Message) -> None:
    """Handles the /all_users_count command."""
    await message.answer(f"👥 {get_all_users_count()}")


async def _send_list_of_users(message: Message, users: List[User]) -> None:
    """Sends a list of the given users."""
    text = ""
    for user in users:
        text += (
            f"🆔 <code>{user.chat_id}</code>\n"
            f"👤 <b>{user.full_name}</b> (@{user.username})\n\n"
        )
    await message.answer(text or "<i>No users found.</i>")


@router.message(IsAdmin(), Command("users"))
async def handle_all_users_command(message: Message) -> None:
    """Handles the /all_users command."""
    await _send_list_of_users(message, get_all_users())


@router.message(IsAdmin(), Command("mailing_users_count"))
async def handle_all_mailing_users_count_command(message: Message) -> None:
    """Handles the /all_mailing_users_count command."""
    await message.answer(f"👥 {get_all_mailing_users_count()}")


@router.message(IsAdmin(), Command("mailing_users"))
async def handle_all_mailing_users_command(message: Message) -> None:
    """Handles the /all_mailing_users command."""
    await _send_list_of_users(message, get_all_mailing_users())


@router.message(IsAdmin(), Command("user"))
@command_argument_required(int)
async def handle_user_command(message: Message, user_chat_id: int) -> None:
    """Handles the /user command."""
    if (user := get_user_by_(user_chat_id)) is None:
        await message.answer("<i>User not found.</i>")
        return
    await message.answer(
        f"🆔 <code>{user.chat_id}</code>\n"
        f"👤 <b>{user.full_name}</b> (@{user.username})\n\n"
        f"🌐 {user.locale}\n"
        f"⏰ {user.timezone}\n"
        f"📦 {user.weather_provider}\n\n"
        f"🗓 {user.created.strftime('%d.%m.%Y %H:%M')}"
    )

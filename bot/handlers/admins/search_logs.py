from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin
from utils.decorators import command_argument_required
from utils.db.crud.search_log import (
    get_all_user_search_logs,
    get_all_user_search_logs_by_,
)


router = Router()


@router.message(IsAdmin(), Command("user_search_logs"))
@command_argument_required(int)
async def handle_user_search_logs_command(
    message: Message, user_chat_id: int
) -> None:
    """Handles the /user_search_logs command."""
    text = ""
    try:
        search_logs = get_all_user_search_logs_by_(
            user_chat_id, locale=message.text.strip().split(" ")[2]
        )
    except IndexError:
        search_logs = get_all_user_search_logs(user_chat_id)

    for search_log in search_logs:
        text += (
            f"🏙 <code>{search_log.city}</code> ({search_log.locale})"
            f" - <b>{search_log.count}</b>\n"
        )
    await message.answer(text or "<i>No search logs found.</i>")

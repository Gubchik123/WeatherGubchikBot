from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin
from utils.decorators import command_argument_required
from utils.db.crud.search_log import get_all_user_search_logs


router = Router()


@router.message(IsAdmin(), Command("user_search_logs"))
@command_argument_required(int)
async def handle_user_search_logs_command(
    message: Message, user_chat_id: int
) -> None:
    """Handles the /user_search_logs command."""
    text = ""
    for search_log in get_all_user_search_logs(user_chat_id):
        text += (
            f"🏙 <code>{search_log.city}</code> ({search_log.locale})"
            f" - <b>{search_log.count}</b>\n"
        )
    await message.answer(text or "<i>No search logs found.</i>")

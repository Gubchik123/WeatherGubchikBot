from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin
from utils.db.crud.search_log import get_all_user_search_logs


router = Router()


@router.message(IsAdmin(), Command("user_search_logs"))
async def handle_user_search_logs_command(message: Message) -> None:
    """Handles the /user_search_logs command."""
    try:
        user_chat_id = int(message.text.split(" ")[1])
    except (ValueError, IndexError):
        await message.answer("Invalid command usage.")
        return
    search_logs = get_all_user_search_logs(user_chat_id)
    text = ""
    for search_log in search_logs:
        text += (
            f"🏙 <code>{search_log.city}</code> ({search_log.locale})"
            f" - <b>{search_log.count}</b>\n"
        )
    await message.answer(text or "No search logs found.")

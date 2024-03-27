from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin
from utils.db.crud.mailing import get_mailing_by_
from utils.decorators import command_argument_required


router = Router()


@router.message(IsAdmin(), Command("amailing"))
@command_argument_required(int)
async def handle_mailing_command(message: Message, user_chat_id: int) -> None:
    """Handles the /mailing command."""
    if (mailing := get_mailing_by_(user_chat_id)) is None:
        await message.answer("<i>Mailing not found.</i>")
        return
    await message.answer(
        f"🆔 <code>{mailing.id_user_id}</code>\n"
        f"🔕 {mailing.mute}\n"
        f"🏙 {mailing.city}\n"
        f"🕒 {mailing.time_int}:00\n"
        f"🗓 {mailing.time_title}"
    )

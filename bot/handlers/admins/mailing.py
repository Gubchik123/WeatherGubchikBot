from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin
from utils.db.crud.mailing import get_mailing_by_


router = Router()


@router.message(IsAdmin(), Command(commands=["amailing"]))
async def handle_mailing_command(message: Message) -> None:
    """Handles the /mailing command."""
    try:
        user_chat_id = int(message.text.split(" ")[1])

        mailing = get_mailing_by_(user_chat_id)
        if mailing is None:
            await message.answer("Mailing not found.")
            return
    except (ValueError, IndexError):
        await message.answer("Invalid command usage.")
        return
    await message.answer(
        f"🆔 <code>{mailing.id_user_id}</code>\n"
        f"🔕 {mailing.mute}\n"
        f"🏙 {mailing.city}\n"
        f"🕒 {mailing.time_int}:00\n"
        f"🗓 {mailing.time_title}"
    )

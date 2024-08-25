from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.decorators import before_handler_clear_state
from filters.is_private_chat_type import IsPrivateChatType

from ..mailing import handle_mailing_menu
from ..mailing.from_command import handle_mailing_command_with_arguments


router = Router()


@router.message(IsPrivateChatType(), Command("mailing"))
@before_handler_clear_state
async def handle_mailing_command(
    message: Message, scheduler: AsyncIOScheduler, **kwargs
):
    """Handles the /mailing command."""
    (
        await handle_mailing_command_with_arguments(message, scheduler)
        if (
            message.chat.type != "private"
            or len(message.text.strip().split(" ")[1:]) == 6
        )
        else await handle_mailing_menu(message)
    )

import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.exceptions import TelegramBadRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import bot
from utils.mock_user import MockUser
from utils.db.crud.user import get_user_by_

from .users.commands.help import handle_help_command
from .users.commands.moon import handle_moon_command
from .users.commands.weather import handle_weather_command
from .users.commands.mailing import handle_mailing_command
from .users.mailing.unsubscribe import unsubscribe_mailing_for_


channels_router = Router()


@channels_router.channel_post(
    F.text.regexp(r"^/(help|moon|weather|mailing|unsubscribe_mailing)@")
)
async def handle_channels_command(
    message: Message, scheduler: AsyncIOScheduler
):
    """Handles the commands in the channels."""
    bot_info = await bot.get_me()
    if bot_info.username not in message.text:
        return

    try:
        await message.delete()
    except TelegramBadRequest as e:
        pass

    command_handler = {
        "help": handle_help_command,
        "moon": handle_moon_command,
        "weather": handle_weather_command,
        "mailing": handle_mailing_command,
        "unsubscribe_mailing": handle_unsubscribe_mailing_command,
    }.get(message.text.split("@")[0][1:])

    try:
        await command_handler(
            message, scheduler=scheduler, state=None, i18n=None
        )
    except TelegramBadRequest as e:
        logging.error(f"in the channel '{message.chat.title}' {str(e)}")


async def handle_unsubscribe_mailing_command(
    message: Message, scheduler: AsyncIOScheduler, **kwargs
):
    """Handles the /unsubscribe_mailing command."""
    user = get_user_by_(message.chat.id)
    unsubscribe_mailing_for_(
        MockUser(
            id=user.chat_id, username=user.username, full_name=user.full_name
        ),
        scheduler,
    )

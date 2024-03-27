import logging
from typing import Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from data.config import ADMINS, BOT_TOKEN


async def notify_admins_on_startup_of_(bot: Bot) -> None:
    """Notifies admins on bot startup."""
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot started!")
        except Exception as err:
            logging.exception(err)


async def send_to_admins(message: str, temp_bot: Optional[Bot] = None):
    """Sends the given message to all admins"""
    is_temp_bot_none = temp_bot is None

    if is_temp_bot_none:
        temp_bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML"),
        )
    for admin in ADMINS:
        await temp_bot.send_message(chat_id=admin, text=message)

    if is_temp_bot_none:
        await temp_bot.session.close()
        del temp_bot

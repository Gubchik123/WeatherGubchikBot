import logging

from aiogram import Bot

from data.config import ADMINS


async def notify_admins(bot: Bot) -> None:
    """Notifies admins on bot startup."""
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot started!")
        except Exception as err:
            logging.exception(err)

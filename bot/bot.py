import os
import logging
from datetime import datetime

from aiogram import executor
from aiogram.utils.exceptions import TelegramAPIError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import handlers
from bot_info import DP
from utils.bot_commands import set_default_commands
from handlers.users.daily_mailing import send_to_users


def set_hours_for_daily_mailing() -> None:
    """For setting daily mailing time by settings timezone"""
    scheduler = AsyncIOScheduler(timezone=str(os.getenv("TIMEZONE")))
    for hour in (6, 9, 12, 15, 18, 21):
        scheduler.add_job(
            send_to_users,
            trigger="cron",
            hour=hour,
            minute=0,
            start_date=datetime.now(),
        )
    scheduler.start()


if __name__ == "__main__":
    set_hours_for_daily_mailing()

    try:
        # Start polling and set default bot commands for three languages
        executor.start_polling(DP, on_startup=set_default_commands)
    except TelegramAPIError as e:
        logger = logging.getLogger("my_logger")
        logger.error(f"Exception during polling: {str(e)}")

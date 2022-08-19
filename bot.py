import schedule
from time import sleep
from threading import Thread

from aiogram import executor

import handlers
from bot_info import DP
from utils.set_bot_commands import set_default_commands
from handlers.users.daily_mailing import mailing_to_users


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(30)


if __name__ == '__main__':
    # Create task at 06:00 for daily mailing and thread for checking loop
    schedule.every().day.at('06:00').do(mailing_to_users)
    Thread(target=schedule_checker, daemon=True).start()
    # Start bot polling and on start set default bot commands for 3 language
    executor.start_polling(DP, on_startup=set_default_commands)

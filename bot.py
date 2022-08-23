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
        sleep(60)


if __name__ == '__main__':
    # Loop for creating tasks at specials hours for daily mailing
    for hour in ("03", "06", "09", "12", "15", "18"):
        schedule.every().day.at(f"{hour}:00").do(mailing_to_users)

    # Other thread for checking loop
    Thread(target=schedule_checker, daemon=True).start()

    # Start bot polling and on start set default bot commands for 3 language
    executor.start_polling(DP, on_startup=set_default_commands)

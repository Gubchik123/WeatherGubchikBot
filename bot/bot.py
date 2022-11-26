import schedule
from time import sleep
from threading import Thread

from aiogram import executor

import handlers
from bot_info import DP
from utils.set_bot_commands import set_default_commands
from handlers.users.daily_mailing import send_to_users


def check_schedule_time():
    while True:
        schedule.run_pending()
        sleep(60)


if __name__ == "__main__":
    # Loop for creating tasks at specials hours for daily mailing
    for hour in ("06", "09", "12", "15", "18", "21"):
        schedule.every().day.at(f"{hour}:00").do(send_to_users)

    # Other thread for checking loop
    Thread(target=check_schedule_time, daemon=True).start()

    # Start bot polling and on start set default bot commands for 3 language
    executor.start_polling(DP, skip_updates=True, on_startup=set_default_commands)

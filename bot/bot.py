import schedule
from time import sleep
from threading import Thread
from datetime import datetime

from aiogram import executor

import handlers
from bot_info import DP
from utils.set_bot_commands import set_default_commands
from handlers.users.daily_mailing import send_to_users


def get_needed_hours():
    return (
        ("04", "07", "10", "13", "16", "19")
        if datetime.now().month in [1, 2, 3, 11, 12]
        else ("03", "06", "09", "12", "15", "18")
    )


def check_schedule_time():
    while True:
        schedule.run_pending()
        sleep(60)


if __name__ == "__main__":
    print(f"Hour in the server: {datetime.now().hour}")

    # Loop for creating tasks at specials hours for daily mailing
    for hour in get_needed_hours():
        schedule.every().day.at(f"{hour}:00").do(send_to_users)

    # Other thread for checking loop
    Thread(target=check_schedule_time, daemon=True).start()

    # Start bot polling and on start set default bot commands for 3 language
    executor.start_polling(DP, skip_updates=True, on_startup=set_default_commands)

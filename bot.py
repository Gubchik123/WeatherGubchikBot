import schedule
from time import sleep
from threading import Thread

from aiogram import executor

from bot_info import DP
import handlers
from handlers.users.daily_mailing import mailing_to_users


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(30)


if __name__ == '__main__':
    schedule.every().day.at('06:00').do(mailing_to_users)
    Thread(target=schedule_checker, daemon=True).start()
    executor.start_polling(DP)

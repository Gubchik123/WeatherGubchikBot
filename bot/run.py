from typing import Union

from aiogram import Dispatcher, F
from aiogram.utils.i18n import I18n
from aiogram.types import ErrorEvent, Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from utils.db.db import Base, engine
from utils.admins import notify_admins_on_startup_of_
from utils.error import send_message_about_error
from utils.bot_commands import set_default_commands_for_
from middlewares import (
    LanguageMiddleware,
    SchedulerMiddleware,
    CallbackQueryTimeoutMiddleware,
)
from data.config import (
    I18N_DOMAIN,
    LOCALES_DIR,
    DEFAULT_LOCALE,
    DEFAULT_TIMEZONE,
    SCHEDULER_JOBS_DATABASE_URL,
)

from bot import bot
from handlers import handlers_router


dispatcher = Dispatcher()

scheduler = AsyncIOScheduler(
    jobstores={
        "default": SQLAlchemyJobStore(
            url=SCHEDULER_JOBS_DATABASE_URL,
            engine=engine,
            tablename="apscheduler_jobs",
            metadata=Base.metadata,
        )
    },
    job_defaults={"misfire_grace_time": 15 * 60},  # 15 minutes
    timezone=DEFAULT_TIMEZONE,
)

i18n = I18n(
    path=LOCALES_DIR, default_locale=DEFAULT_LOCALE, domain=I18N_DOMAIN
)


@dispatcher.error(
    F.update.message.as_("event") | F.update.callback_query.as_("event")
)
async def handle_all_errors(
    error_event: ErrorEvent, event: Union[Message, CallbackQuery]
):
    """Handles all errors."""
    error = error_event.exception
    await send_message_about_error(
        event, str(error), error_place=f" {str(error.__class__)[8:-2]}"
    )


@dispatcher.startup()
async def on_startup() -> None:
    """Runs useful functions on bot startup."""
    Base.metadata.create_all(bind=engine)

    scheduler.start()
    scheduler.print_jobs()

    _register_routers()
    _register_middlewares()
    await set_default_commands_for_(bot)
    await notify_admins_on_startup_of_(bot)


def _register_routers() -> None:
    dispatcher.include_router(handlers_router)


def _register_middlewares() -> None:
    LanguageMiddleware(i18n).setup(dispatcher)
    # Message middleware
    dispatcher.message.middleware(SchedulerMiddleware(scheduler))
    # CallbackQuery middlewares
    dispatcher.callback_query.middleware(CallbackQueryTimeoutMiddleware())
    dispatcher.callback_query.middleware(SchedulerMiddleware(scheduler))


if __name__ == "__main__":
    dispatcher.run_polling(bot)

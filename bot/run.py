from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from utils.db.db import Base, engine
from utils.notify_admins import notify_admins
from utils.bot_commands import set_default_bot_commands
from middlewares import (
    LanguageMiddleware,
    SchedulerMiddleware,
    CallbackQueryTimeoutMiddleware,
)
from data.config import (
    BOT_TOKEN,
    I18N_DOMAIN,
    LOCALES_DIR,
    DEFAULT_LOCALE,
    DEFAULT_TIMEZONE,
    SCHEDULER_JOBS_DATABASE_URL,
)

from handlers import handlers_router


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
)
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


def _register_routers() -> None:
    dispatcher.include_router(handlers_router)


def _register_middlewares() -> None:
    dispatcher.message.outer_middleware(LanguageMiddleware(i18n))
    dispatcher.message.middleware(SchedulerMiddleware(scheduler))

    dispatcher.callback_query.middleware(LanguageMiddleware(i18n))
    dispatcher.callback_query.middleware(SchedulerMiddleware(scheduler))
    dispatcher.callback_query.middleware(CallbackQueryTimeoutMiddleware())


@dispatcher.startup()
async def on_startup() -> None:
    """Runs useful functions on bot startup."""
    Base.metadata.create_all(bind=engine)

    scheduler.start()
    scheduler.print_jobs()

    _register_routers()
    _register_middlewares()
    await set_default_bot_commands(bot)
    await notify_admins(bot)


if __name__ == "__main__":
    dispatcher.run_polling(bot)

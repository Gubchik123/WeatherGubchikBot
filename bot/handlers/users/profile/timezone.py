from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.db.crud.mailing import get_mailing_by_
from utils.db.crud.user import update_user_with_
from keyboards.inline.profile.timezone import (
    get_countries_keyboard,
    get_cities_keyboard,
)

from .menu import handle_profile


router = Router()


@router.callback_query(F.data == "btn_timezone")
async def send_countries(callback_query: CallbackQuery, *args) -> None:
    """Sends countries to choose from."""
    await callback_query.message.edit_text(
        text=_(
            "<b>Changing timezone.</b>\n\n"
            "You can choose a new time zone by choosing from the options below."
        ),
        reply_markup=get_countries_keyboard(),
    )


@router.callback_query(F.data.regexp(r"^timezone:\w*:$"))
async def send_cities(callback_query: CallbackQuery) -> None:
    """Sends cities of the selected country to choose from."""
    country = callback_query.data.split(":")[1]
    await callback_query.message.edit_text(
        text=_("Choose a city in {country}:").format(country=country),
        reply_markup=get_cities_keyboard(country),
    )


@router.callback_query(F.data.regexp(r"^timezone:\w*:\w*"))
async def change_timezone(
    callback_query: CallbackQuery, scheduler: AsyncIOScheduler
) -> None:
    """Changes user's timezone."""
    country, city = callback_query.data.split(":")[1:]
    timezone = f"{country}/{city}"

    update_user_with_(callback_query.from_user.id, timezone=timezone)
    _update_mailing_job_for_(callback_query.from_user.id, timezone, scheduler)

    await callback_query.answer(
        text=_("Timezone successfully changed to {timezone}!").format(
            timezone=timezone
        )
    )
    await handle_profile(callback_query)


def _update_mailing_job_for_(
    user_id: int, timezone: str, scheduler: AsyncIOScheduler
) -> None:
    """Updates the mailing job for the user."""
    job: Job = scheduler.get_job(f"mailing-{user_id}")
    if job:
        mailing = get_mailing_by_(user_id)
        job.reschedule(
            trigger="cron",
            timezone=timezone,
            hour=mailing.time_int,
            minute=30,
            second=0,
        )

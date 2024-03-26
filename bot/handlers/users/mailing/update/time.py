from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.db.crud.user import get_user_by_
from utils.db.crud.mailing import update_mailing_with_
from states.mailing_setup import MailingSetup

from ..menu import handle_mailing_menu


router = Router()


@router.callback_query(
    MailingSetup.time, F.data.startswith("btn_mailing_time_int:")
)
async def handle_update_mailing_time(
    callback_query: CallbackQuery,
    state: FSMContext,
    scheduler: AsyncIOScheduler,
):
    """Handles updating the mailing time."""
    await state.clear()

    user_chat_id = callback_query.from_user.id
    time_int = int(callback_query.data.split(":")[-1])

    update_mailing_with_(user_chat_id, time_int=time_int)
    _reschedule_mailing(user_chat_id, time_int, scheduler)

    await callback_query.answer(
        _("The mailing time has been successfully updated!"),
    )
    await handle_mailing_menu(callback_query)


def _reschedule_mailing(
    user_chat_id: int, time_int: int, scheduler: AsyncIOScheduler
) -> None:
    """Reschedules the mailing."""
    user = get_user_by_(user_chat_id)

    job: Job = scheduler.get_job(f"mailing-{user_chat_id}")

    if job:
        job.reschedule(
            trigger="cron",
            hour=time_int,
            minute=0,
            second=0,
            timezone=user.timezone,
        )

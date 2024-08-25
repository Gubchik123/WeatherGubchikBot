import asyncio

from aiogram import Router, F
from aiogram.utils.i18n import gettext as _
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import CallbackQuery, User as TelegramUser
from sqlalchemy.orm.exc import UnmappedInstanceError
from apscheduler.jobstores.base import JobLookupError

from utils.admins import ADMINS, send_to_admins
from utils.db.crud.mailing import delete_mailing_for_
from keyboards.inline.maker import make_yes_or_no_inline_keyboard

from ..menu import handle_menu


router = Router()


@router.callback_query(F.data == "btn_mailing_unsubscribe")
async def ask_about_unsubscribe(callback_query: CallbackQuery):
    """Asks user to confirm the unsubscription from the mailing."""
    await callback_query.message.edit_text(
        _("Are you sure you want to unsubscribe from the mailing?"),
        reply_markup=make_yes_or_no_inline_keyboard(
            yes_callback_data="btn_mailing_unsubscribe_confirm",
            no_callback_data="btn_mailing",
        ),
    )


@router.callback_query(F.data == "btn_mailing_unsubscribe_confirm")
async def handle_unsubscribe(
    callback_query: CallbackQuery, scheduler: AsyncIOScheduler
):
    """Handles the user unsubscription from the mailing."""
    unsubscribe_mailing_for_(
        user=callback_query.from_user, scheduler=scheduler
    )
    await callback_query.answer(
        _("You have successfully unsubscribed from the mailing!")
    )
    await handle_menu(callback_query)


def unsubscribe_mailing_for_(user: TelegramUser, scheduler: AsyncIOScheduler):
    """Unsubscribes the given user from the mailing."""
    try:
        remove_mailing_for_(user.id, scheduler)
    except (UnmappedInstanceError, JobLookupError):
        return
    if user.id not in ADMINS:
        asyncio.create_task(
            send_to_admins(
                f"❌📨 {user.full_name} (<code>{user.id}</code>) "
                "unsubscribe from mailing."
            )
        )


def remove_mailing_for_(user_id: int, scheduler: AsyncIOScheduler):
    """Removes the mailing for the user."""
    delete_mailing_for_(user_id)
    scheduler.remove_job(f"mailing-{user_id}")

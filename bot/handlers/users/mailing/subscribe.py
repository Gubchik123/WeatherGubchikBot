import asyncio
from datetime import datetime
from pytz import timezone as tz

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import I18n, gettext as _
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.scheduler import send_mailing
from utils.admins import ADMINS, send_to_admins
from utils.db.crud.user import get_user_by_
from utils.db.crud.mailing import create_mailing_for_
from utils.decorators import before_handler_clear_state
from keyboards.inline.mailing import get_mailing_time_inline_keyboard
from states.utils import get_state_class_by_
from states.mailing_subscription import MailingSubscription

from .menu import handle_mailing_menu
from ..weather.city import ask_about_city


router = Router()


@router.callback_query(F.data == "btn_subscribe_mailing")
@before_handler_clear_state
async def handle_subscribe_mailing(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18n, **kwargs
):
    """Starts the mailing subscription state."""
    await ask_about_city(callback_query, i18n)
    await state.set_state(MailingSubscription.city)


@router.callback_query(
    MailingSubscription.mute, F.data.startswith("btn_mailing_mute:")
)
async def check_mute_mode(callback_query: CallbackQuery, state: FSMContext):
    """Processes the selected mute mode for the mailing."""
    await state.update_data({"mute": callback_query.data.endswith("yes")})
    await ask_about_mailing_time(callback_query, state)
    await state.set_state(MailingSubscription.time)


@router.callback_query(F.data == "btn_mailing_time_int")
async def ask_about_mailing_time(
    callback_query: CallbackQuery, state: FSMContext
):
    """Asks user to choose the time for the mailing."""
    # TODO: Allow user to enter the time manually
    await callback_query.message.edit_text(
        _("At what time would you like to receive the newsletter?"),
        reply_markup=get_mailing_time_inline_keyboard(),
    )
    state_class = await get_state_class_by_(state)
    await state.set_state(state_class.time)


@router.callback_query(
    MailingSubscription.time, F.data.startswith("btn_mailing_time_int:")
)
async def check_mailing_time(
    callback_query: CallbackQuery,
    state: FSMContext,
    scheduler: AsyncIOScheduler,
):
    """Processes the selected time for the mailing."""
    await state.update_data(
        {"time_int": int(callback_query.data.split(":")[-1])}
    )
    data = await state.get_data()
    _subscribe_mailing(callback_query.message.chat.id, data, scheduler)
    await state.clear()

    await callback_query.answer(
        _("You have successfully completed the mailing setup!"),
    )
    await handle_mailing_menu(callback_query)

    user = callback_query.from_user
    if user.id not in ADMINS:
        asyncio.create_task(
            send_to_admins(
                f"🆕📨 {user.full_name} (<code>{user.id}</code>) "
                f"subscribe to mailing."
            )
        )


def _subscribe_mailing(
    user_chat_id: int, data: dict, scheduler: AsyncIOScheduler
):
    """Enables the mailing."""
    user = get_user_by_(user_chat_id)
    create_mailing_for_(user.chat_id, data)
    scheduler.add_job(
        send_mailing,
        trigger="cron",
        hour=data["time_int"],
        minute=0,
        second=0,
        timezone=user.timezone,
        id=f"mailing-{user.chat_id}",
        args=[user.chat_id],
        start_date=datetime.now(tz(user.timezone)),
    )

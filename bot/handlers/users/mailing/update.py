from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from states.mailing_setup import MailingSetup
from utils.db.crud.user import get_user_by_
from utils.weather.search import get_searched_data_with_
from utils.db.crud.mailing import (
    update_mailing_with_,
    update_mailing_period,
    update_mailing_city,
)

from .menu import handle_mailing_menu
from ..weather.city import ask_about_city
from ..weather.city_title import ask_about_city_title


router = Router()


@router.callback_query(
    MailingSetup.mute, F.data.startswith("btn_mailing_mute:")
)
async def handle_update_mailing_mute(
    callback_query: CallbackQuery, state: FSMContext
):
    """Handles updating the mailing mute mode."""
    await state.clear()
    mute = callback_query.data.endswith("yes")

    update_mailing_with_(callback_query.from_user.id, mute=mute)

    message = (
        _("The mailing has been muted!")
        if mute
        else _("The mailing has been unmuted!")
    )
    await callback_query.answer(message)
    await handle_mailing_menu(callback_query)


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


@router.callback_query(MailingSetup.period, F.data.startswith("btn_period:"))
async def handle_update_mailing_period(
    callback_query: CallbackQuery, state: FSMContext
):
    """Processes the selected period of the weather forecast."""
    await state.clear()
    time_title, time = callback_query.data.split(":")[1:]

    update_mailing_period(
        callback_query.from_user.id,
        data={
            "time": time,
            "time_title": time_title,
            "type": "weather" if time != "review" else time,
        },
    )
    await callback_query.answer(
        _("The mailing period has been successfully updated!"),
    )
    await handle_mailing_menu(callback_query)


@router.callback_query(F.data == "btn_mailing_city")
async def handle_mailing_city(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18n
):
    """Starts the mailing city state."""
    await ask_about_city(callback_query, i18n)
    await state.set_state(MailingSetup.city)


@router.message(MailingSetup.city, F.text)
async def handle_update_mailing_city(
    message: Message, state: FSMContext, i18n: I18n
):
    """Requests search city and checks it."""
    city = message.text.lower()
    searching_message = await message.answer(_("Searching..."))

    result, is_match_100 = get_searched_data_with_(
        message.text.lower(), i18n.current_locale
    )
    if is_match_100:
        await state.clear()
        await _handle_update_mailing_city(
            message, city=result, city_title=city.capitalize()
        )
    else:
        await state.set_data({"search_cities": result})
        await ask_about_city_title(message, state)

    await searching_message.delete()


@router.callback_query(MailingSetup.city, F.data.startswith("btn_city_title:"))
async def handle_update_mailing_city_title(
    callback_query: CallbackQuery, state: FSMContext, i18n: I18n
):
    """Handles updating the mailing city."""
    await state.clear()

    city = callback_query.data.split(":")[-1].strip().lower()
    city = city.split("(")[0].strip()
    result, is_match_100 = get_searched_data_with_(city, i18n.current_locale)

    update_mailing_city(
        callback_query.from_user.id, city=result, city_title=city.capitalize()
    )
    await callback_query.answer(
        _("The mailing city has been successfully updated!"),
    )
    await handle_mailing_menu(callback_query)


async def _handle_update_mailing_city(
    event: Union[Message, CallbackQuery], city: str, city_title: str
):
    """Updates the mailing city."""
    update_mailing_city(event.from_user.id, city=city, city_title=city_title)

    if isinstance(event, CallbackQuery):
        await event.answer(
            _("The mailing city has been successfully updated!"),
        )
    await handle_mailing_menu(event)

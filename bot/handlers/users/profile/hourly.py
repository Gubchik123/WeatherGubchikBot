from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from utils.db.crud.user import update_user_with_, get_user_by_

from .menu import handle_profile


router = Router()


@router.callback_query(F.data == "btn_toggle_hourly")
async def handle_toggle_hourly(callback_query: CallbackQuery):
    """Toggles the hourly forecast mode for the user."""
    user = get_user_by_(callback_query.from_user.id)
    new_hourly_value = not user.hourly

    update_user_with_(callback_query.from_user.id, hourly=new_hourly_value)

    message = (
        _(
            "Hourly forecast enabled! You'll now see hourly weather for today and tomorrow."
        )
        if new_hourly_value
        else _(
            "Hourly forecast disabled! You'll now see regular daily forecasts."
        )
    )
    await callback_query.answer(message, show_alert=True)
    await handle_profile(callback_query)

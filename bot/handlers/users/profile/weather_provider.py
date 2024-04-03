from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from utils.db.crud.user import change_user_weather_provider_by_
from keyboards.inline.weather_provider import (
    get_weather_provider_inline_keyboard,
)

from .menu import handle_profile


router = Router()


@router.callback_query(F.data == "btn_weather_provider")
async def handle_change_weather_provider(callback_query: CallbackQuery):
    """Asks the user to choose a weather provider."""
    await callback_query.message.edit_text(
        text=_(
            "<b>Changing weather provider.</b>\n\n"
            "You can choose a new weather provider below:"
        ),
        reply_markup=get_weather_provider_inline_keyboard(),
    )


@router.callback_query(F.data.startswith("btn_weather_provider:"))
async def handle_change_weather_provider(callback_query: CallbackQuery):
    """Handles changing weather provider."""
    weather_provider = callback_query.data.split(":")[-1]
    change_user_weather_provider_by_(
        callback_query.from_user.id, weather_provider=weather_provider
    )
    await callback_query.answer(
        text=_(
            "Weather provider successfully changed to {weather_provider}!"
        ).format(weather_provider=weather_provider)
    )
    await handle_profile(callback_query)

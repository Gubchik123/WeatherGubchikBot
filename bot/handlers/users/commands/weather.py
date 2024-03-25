from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import I18n
from aiogram.fsm.context import FSMContext

from ..weather.city import ask_about_city


router = Router()


@router.message(Command(commands=["weather"]))
async def handle_weather_command(
    message: Message, state: FSMContext, i18n: I18n
):
    """Handles the /weather command."""
    await ask_about_city(message, state, i18n)

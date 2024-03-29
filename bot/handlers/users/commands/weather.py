from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import I18n
from aiogram.fsm.context import FSMContext

from utils.decorators import before_command_clear_state

from ..weather.city import handle_weather


router = Router()


@router.message(Command("weather"))
@before_command_clear_state
async def handle_weather_command(
    message: Message, state: FSMContext, i18n: I18n
):
    """Handles the /weather command."""
    await handle_weather(message, state, i18n)

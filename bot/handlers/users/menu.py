from typing import Union

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from keyboards.default.menu import get_menu_keyboard


router = Router()


@router.message(Command("menu"))
@router.callback_query(F.data == "btn_menu")
async def handle_menu(event: Union[Message, CallbackQuery]) -> None:
    """Handles main menu."""
    is_callback_query = isinstance(event, CallbackQuery)
    message = event.message if is_callback_query else event

    if is_callback_query:
        await message.delete()
    await message.answer(
        _(
            "You are in the main menu.\nSelect further actions with the buttons below."
        ),
        reply_markup=get_menu_keyboard(),
    )

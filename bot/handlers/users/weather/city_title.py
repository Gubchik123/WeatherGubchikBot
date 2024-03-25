from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from states.utils import get_state_class_by_
from keyboards.inline.weather import get_cities_inline_keyboard

from .period import ask_about_period


router = Router()


async def ask_about_city_title(message: Message, state: FSMContext) -> None:
    """Asks user to choose the city title from the list."""
    data: dict = await state.get_data()
    await message.answer(
        _("Choose the city / locality you had in mind:"),
        reply_markup=get_cities_inline_keyboard(
            cities=data["search_cities"].keys()
        ),
    )
    state_class = await get_state_class_by_(state)
    await state.set_state(state_class.city_title)


@router.callback_query(F.data.startswith("btn_city_title:"))
async def process_city_title(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    """Processes the city title from the state search list."""
    data: dict = await state.get_data()
    city_title = callback_query.data.split(":")[-1]

    await state.update_data(
        {
            "city": data["search_cities"][city_title],
            "city_title": city_title.capitalize(),
        }
    )
    await ask_about_period(callback_query, state)

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _

from utils.db.crud.user import get_user_by_
from states.utils import get_state_class_by_
from utils.weather import get_weather_provider_module_by_
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
    if state_class:
        await state.set_state(state_class.city_title)


@router.callback_query(F.data.startswith("btn_city_title:"))
async def check_city_callback_query(
    event: CallbackQuery, i18n: I18n, state: FSMContext
):
    """Requests search city and checks it."""
    city = _get_city_from_(event.data)

    user = get_user_by_(event.from_user.id)
    weather_provider_module = get_weather_provider_module_by_(
        user.weather_provider
    )
    result, _ = await weather_provider_module.get_searched_data_with_(
        city, i18n.current_locale
    )
    await state.update_data({"city": result, "city_title": city.capitalize()})
    await ask_about_period(event, state)


def _get_city_from_(event_data: str) -> str:
    """Returns city from the given event data."""
    city = event_data.split(":")[-1].strip().lower()
    city = city.split("(")[0].strip()
    return _strip_emoji_from_(city)


def _strip_emoji_from_(city: str) -> str:
    """Returns city without emoji at the beginning if it is there."""
    emoji_ranges = (("\U0001F1E0", "\U0001F1FF"),)  # flags
    while city and any(start <= city[0] <= end for start, end in emoji_ranges):
        city = city[1:]
    return city.strip()

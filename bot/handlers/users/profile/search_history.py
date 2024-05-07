from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import I18n, gettext as _

from utils.services import get_city_from_
from states.search_history import SearchHistory
from keyboards.inline.weather import get_cities_with_delete_inline_keyboard
from utils.db.crud.search_log import (
    get_last_search_cities_by_,
    delete_search_cities,
)

from .menu import handle_profile


router = Router()


@router.callback_query(F.data == "btn_search_history")
async def handle_search_history(
    event: CallbackQuery, state: FSMContext, i18n: I18n
) -> None:
    """Handles user search history."""
    last_search_cities = get_last_search_cities_by_(
        event.from_user.id, i18n.current_locale
    )
    if not last_search_cities:
        await event.answer(_("You have no search history yet."))
        return
    await state.set_state(SearchHistory.city)
    await state.update_data(cities=last_search_cities)
    await event.message.edit_text(
        _("Select cities from your search history you want to delete:"),
        reply_markup=get_cities_with_delete_inline_keyboard(
            last_search_cities
        ),
    )


@router.callback_query(
    SearchHistory.city, F.data.startswith("btn_city_title:")
)
async def handle_search_history_city(
    event: CallbackQuery, state: FSMContext
) -> None:
    """Handles user search history city."""
    city = get_city_from_(event.data).title()

    data = await state.get_data()
    cities = data["cities"]
    cities[cities.index(city)] = f"✅ {city}" if "✅" not in city else city[2:]

    await state.update_data(cities=cities)
    await event.message.edit_reply_markup(
        inline_message_id=event.inline_message_id,
        reply_markup=get_cities_with_delete_inline_keyboard(cities),
    )


@router.callback_query(
    SearchHistory.city, F.data.startswith("btn_delete_selected_search_cities")
)
async def handle_delete_selected_search_cities(
    event: CallbackQuery, state: FSMContext, i18n: I18n
) -> None:
    """Handles deleting selected search cities."""
    data = await state.get_data()
    selected_cities = [city[2:] for city in data["cities"] if "✅" in city]
    if not selected_cities:
        await event.answer(_("No cities selected."))
        return
    await state.clear()

    delete_search_cities(
        event.from_user.id, selected_cities, i18n.current_locale
    )
    await event.answer(_("Selected cities deleted."))
    await handle_profile(event)

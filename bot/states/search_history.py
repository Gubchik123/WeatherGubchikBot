from aiogram.fsm.state import State, StatesGroup


class SearchHistory(StatesGroup):
    """States for search history."""

    city = State()

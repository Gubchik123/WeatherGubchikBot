from aiogram.dispatcher.filters.state import State, StatesGroup


class Choosing(StatesGroup):
    """For storing temp info for weather searching"""

    language = State()

    region = State()
    region_title = State()
    period = State()

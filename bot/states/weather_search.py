from aiogram.fsm.state import State, StatesGroup


class WeatherSearch(StatesGroup):
    """States for weather search."""

    city = State()
    city_title = State()
    period = State()

from aiogram.fsm.state import State

from .weather_search import WeatherSearch


class MailingSetup(WeatherSearch):
    """States to enable mailing."""

    city = State()
    city_title = State()
    period = State()
    mute = State()
    time = State()

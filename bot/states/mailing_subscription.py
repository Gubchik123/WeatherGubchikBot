from aiogram.fsm.state import State

from .weather_search import WeatherSearch


class MailingSubscription(WeatherSearch):
    """States to subscribe to the mailing."""

    city = State()
    city_title = State()
    period = State()
    mute = State()
    time = State()

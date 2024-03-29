from aiogram.fsm.state import State, StatesGroup


class MailingSubscription(StatesGroup):
    """States to subscribe to the mailing."""

    city = State()
    city_title = State()
    period = State()
    mute = State()
    time = State()

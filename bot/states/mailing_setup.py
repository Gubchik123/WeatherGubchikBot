from aiogram.fsm.state import State, StatesGroup


class MailingSetup(StatesGroup):
    """States to set up the mailing."""

    city = State()
    city_title = State()
    period = State()
    mute = State()
    time = State()

from aiogram.dispatcher.filters.state import State, StatesGroup


class Mailing(StatesGroup):
    """For storing temp info for different mailing actions"""

    # States for turning on mailing
    turn_on = State()
    mute_mode = State()
    time = State()
    # States for changing info about mailing
    turn_on_mute_mode = State()
    turn_off_mute_mode = State()
    change_city = State()
    change_period = State()
    change_time = State()
    # States for turning off mailing
    turn_off = State()

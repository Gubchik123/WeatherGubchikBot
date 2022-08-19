from aiogram.dispatcher.filters.state import State, StatesGroup


class Mailing(StatesGroup):
    # States for turning on mailing
    turn_on = State()
    mute_mode = State()
    # States for changing info about mailing
    turn_on_mute_mode = State()
    turn_off_mute_mode = State()
    change_city = State()
    # States for turning off mailing
    turn_off = State()

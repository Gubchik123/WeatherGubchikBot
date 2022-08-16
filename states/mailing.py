from aiogram.dispatcher.filters.state import State, StatesGroup


class Mailing(StatesGroup):
    turn_on = State()
    mute_mode = State()
    turn_off = State()

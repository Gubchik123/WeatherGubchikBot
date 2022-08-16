from aiogram.dispatcher.filters.state import State, StatesGroup


class Choosing(StatesGroup):
    region = State()
    city = State()
    period = State()

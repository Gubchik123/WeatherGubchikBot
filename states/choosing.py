from aiogram.dispatcher.filters.state import State, StatesGroup


class Choosing(StatesGroup):
    region = State()
    district = State()
    district_letter = State()
    city = State()
    period = State()

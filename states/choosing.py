from aiogram.dispatcher.filters.state import State, StatesGroup


class Choosing(StatesGroup):
    language = State()

    region = State()
    region_title = State()
    period = State()

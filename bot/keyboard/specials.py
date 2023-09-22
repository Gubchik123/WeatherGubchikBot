from aiogram import types
from constants import TEXT
from .default import make_keyboard, make_button


def make_keyboard_for_yes_or_no_answer() -> types.ReplyKeyboardMarkup:
    """For getting keyboard with agree and decline buttons"""
    markup = make_keyboard(width=2, one_time=True)
    markup.add(make_button(TEXT().yes_btn()), make_button(TEXT().no_btn()))
    return markup


def make_weather_forecast_keyboard() -> types.ReplyKeyboardMarkup:
    """For getting keyboard with buttons for searching weather information"""
    markup = make_keyboard(width=2, one_time=True)
    markup.add(make_button(TEXT().weather_forecast_btn()))
    return markup

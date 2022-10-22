from constants import TEXT

from .default import make_keyboard, make_button


def make_keyboard_for_yes_or_no_answer():
    global TEXT
    markup = make_keyboard(width=2, one_time=True)
    markup.add(
        make_button(TEXT().yes_btn()),
        make_button(TEXT().no_btn())
    )
    return markup


def make_keyboard_for_country_choosing():
    global TEXT
    markup = make_keyboard(width=2, one_time=True)
    markup.add(
        make_button(TEXT().weather_in_Ukraine_btn()),
        make_button(TEXT().weather_in_Europe_btn())
    )
    return markup

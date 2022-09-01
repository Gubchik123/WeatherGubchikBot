from .default import make_keyboard, make_button


def make_keyboard_for_yes_or_no_answer():
    markup = make_keyboard(width=2, one_time=True)
    markup.add(
        make_button("Так"),
        make_button("Ні")
    )
    return markup


def make_keyboard_for_country_choosing():
    markup = make_keyboard(width=2, one_time=True)
    markup.add(
        make_button("Погода в Україні"),
        make_button("Погода в Європі")
    )
    return markup

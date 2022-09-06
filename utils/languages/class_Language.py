from googletrans import Translator

from .class_UA import UA
from .class_OtherLanguage import OtherLanguage


class Language(UA):
    def __init__(self):
        self.__lang: UA | OtherLanguage = None

    @property
    def lang_code(self): return self.__lang.lang

    def change_on(self, lang_code: str) -> UA | OtherLanguage:
        self.__lang = UA(lang_code) if lang_code == "uk" \
            else OtherLanguage(lang_code)

    def change_on_detected_language_from(self, text: str):
        detected = Translator().detect(text)

        if detected.lang != self.lang_code:
            self.change_on(detected.lang)

    def hello_message(self, name: str): return self.__lang.hello_message(name)

    def goodbye_message(self, name: str):
        return self.__lang.goodbye_message(name)

    def general_rules(self): return self.__lang.general_rules()

    def yes_btn(self): return self.__lang.yes_btn()

    def no_btn(self): return self.__lang.no_btn()

    def weather_in_Ukraine_btn(
        self): return self.__lang.weather_in_Ukraine_btn()

    def weather_in_Europe_btn(self): return self.__lang.weather_in_Europe_btn()

    def back_to_menu_btn(self): return self.__lang.back_to_menu_btn()

    def menu_btn_mailing_managment(self):
        return self.__lang.menu_btn_mailing_managment()

    def menu_btn_turn_on_mailing(self):
        return self.__lang.menu_btn_turn_on_mailing()

    def menu_btn_goodbye(self): return self.__lang.menu_btn_goodbye()

    def menu_message(self): return self.__lang.menu_message()

    def choose_region_message(self):
        return self.__lang.choose_region_message()

    def repeat_choosing_btn(self): return self.__lang.repeat_choosing_btn()

    def choose_minded_option(self):
        return self.__lang.choose_minded_option()

    def there_are_not_such_type_of_region_message(self):
        return self.__lang.there_are_not_such_type_of_region_message()

    def today_btn(self): return self.__lang.today_btn()
    def tomorrow_btn(self): return self.__lang.tomorrow_btn()
    def week_btn(self): return self.__lang.week_btn()
    def two_week_btn(self): return self.__lang.two_week_btn()

    def choose_period_message(self): return self.__lang.choose_period_message()

    def there_are_not_such_type_of_period_message(self):
        return self.__lang.there_are_not_such_type_of_period_message()

    def error_message(self): return self.__lang.error_message()

    def mute_mode_btn(self): return self.__lang.mute_mode_btn()
    def unmute_mode_btn(self): return self.__lang.unmute_mode_btn()

    def change_mailing_time_btn(self):
        return self.__lang.change_mailing_time_btn()

    def change_mailing_city_btn(self):
        return self.__lang.change_mailing_city_btn()

    def change_mailing_period_btn(self):
        return self.__lang.change_mailing_period_btn()

    def turn_off_mailing_btn(self):
        return self.__lang.turn_off_mailing_btn()

    def daily_mailing_message(self): return self.__lang.daily_mailing_message()

    def what_do_you_want_to_do_with_mailing_message(self):
        return self.__lang.what_do_you_want_to_do_with_mailing_message()

    def turn_on_mailing_question_message(self):
        return self.__lang.turn_on_mailing_question_message()

    def turn_off_mailing_question_message(self):
        return self.__lang.turn_off_mailing_question_message()

    def change_mailing_city_question_message(self):
        return self.__lang.change_mailing_city_question_message()

    def change_mailing_period_question_message(self):
        return self.__lang.change_mailing_period_question_message()

    def what_mailing_time_question_message(self):
        return self.__lang.what_mailing_time_question_message()

    def mailing_mute_mode_question_message(self):
        return self.__lang.mailing_mute_mode_question_message()

    def ok_action_canceled_message(self): 
        return self.__lang.ok_action_canceled_message()

    def there_are_not_such_type_of_answer_message(self):
        return self.__lang.there_are_not_such_type_of_answer_message()

    def choose_weather_country_question_message(self):
        return self.__lang.choose_weather_country_question_message()

    def choose_mailing_country_question_message(self):
        return self.__lang.choose_mailing_country_question_message()

    def successfully_turn_on_mailing_message(self):
        return self.__lang.successfully_turn_on_mailing_message()

    def successfully_turn_off_mailing_message(self):
        return self.__lang.successfully_turn_off_mailing_message()

    def unmute_mailing_mode_question_message(self):
        return self.__lang.unmute_mailing_mode_question_message()

    def mute_mailing_mode_question_message(self):
        return self.__lang.mute_mailing_mode_question_message()

    def change_mailing_time_question_message(self):
        return self.__lang.change_mailing_time_question_message()

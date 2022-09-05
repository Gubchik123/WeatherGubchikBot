from googletrans import Translator

from .class_UA import UA

translator = Translator()


class OtherLanguage(UA):
    def __init__(self, lang_code: str):
        super().__init__(lang_code)

    def _translated_(self, func) -> str:
        translation = translator.translate(func(), dest=self.lang_code)
        return translation.text

    def hello_message(self, name: str):
        translation = translator.translate(super().hello_message(name),
                                           dest=self.lang_code)
        return translation.text

    def goodbye_message(self, name: str):
        translation = translator.translate(super().goodbye_message(name),
                                           dest=self.lang_code)
        return translation.text

    def general_rules(self):
        return self._translated_(super().general_rules)

    def yes_btn(self): 
        return self._translated_(
            super().yes_btn).replace("So", "Yes").replace("Так", "Да")

    def no_btn(self): return self._translated_(super().no_btn)

    def weather_in_Ukraine_btn(self):
        return self._translated_(
            super().weather_in_Ukraine_btn
        ).capitalize().replace("The w", 'W').replace("u", "U").replace("у", "У")

    def weather_in_Europe_btn(self):
        return self._translated_(super().weather_in_Europe_btn)

    def back_to_menu_btn(self):
        return self._translated_(super().back_to_menu_btn)

    def menu_btn_mailing_managment(self):
        return self._translated_(super().menu_btn_mailing_managment)

    def menu_btn_turn_on_mailing(self):
        return self._translated_(super().menu_btn_turn_on_mailing)

    def menu_btn_goodbye(self):
        return self._translated_(super().menu_btn_goodbye)

    def menu_message(self):
        return self._translated_(super().menu_message)

    def choose_region_message(self):
        return self._translated_(super().choose_region_message)

    def repeat_choosing_btn(self): return self._translated_(
        super().repeat_choosing_btn)

    def choose_minded_option(self):
        return self._translated_(super().choose_minded_option)

    def there_are_not_such_type_of_region_message(self):
        return self._translated_(super().there_are_not_such_type_of_region_message)

    def today_btn(self): return self._translated_(
        super().today_btn)

    def tomorrow_btn(self): return self._translated_(
        super().tomorrow_btn)

    def week_btn(self): return self._translated_(
        super().week_btn).replace('w', 'W')

    def two_week_btn(self): return self._translated_(
        super().two_week_btn)

    def choose_period_message(self): return self._translated_(
        super().choose_period_message)

    def there_are_not_such_type_of_period_message(self):
        return self._translated_(super().there_are_not_such_type_of_period_message)

    def error_message(self):
        return self._translated_(super().error_message)

    def mute_mode_btn(self):
        return self._translated_(super().mute_mode_btn)

    def unmute_mode_btn(self):
        return self._translated_(super().unmute_mode_btn)

    def change_mailing_time_btn(self):
        return self._translated_(super().change_mailing_time_btn)

    def change_mailing_city_btn(self):
        return self._translated_(super().change_mailing_city_btn)

    def change_mailing_period_btn(self):
        return self._translated_(super().change_mailing_period_btn)

    def turn_off_mailing_btn(self):
        return self._translated_(super().turn_off_mailing_btn)

    def daily_mailing_message(self):
        return self._translated_(super().daily_mailing_message)

    def what_do_you_want_to_do_with_mailing_message(self):
        return self._translated_(super().what_do_you_want_to_do_with_mailing_message)

    def turn_on_mailing_question_message(self):
        return self._translated_(super().turn_on_mailing_question_message)

    def turn_off_mailing_question_message(self):
        return self._translated_(super().turn_off_mailing_question_message)

    def change_mailing_city_question_message(self):
        return self._translated_(super().change_mailing_city_question_message)

    def change_mailing_period_question_message(self):
        return self._translated_(super().change_mailing_period_question_message)

    def what_mailing_time_question_message(self):
        return self._translated_(super().what_mailing_time_question_message)

    def mailing_mute_mode_question_message(self):
        return self._translated_(super().mailing_mute_mode_question_message)

    def ok_action_canceled_message(self):
        return self._translated_(super().ok_action_canceled_message)

    def there_are_not_such_type_of_answer_message(self):
        return self._translated_(super().there_are_not_such_type_of_answer_message)

    def choose_weather_country_question_message(self):
        return self._translated_(super().choose_weather_country_question_message)

    def choose_mailing_country_question_message(self):
        return self._translated_(super().choose_mailing_country_question_message)

    def successfully_turn_on_mailing_message(self):
        return self._translated_(super().successfully_turn_on_mailing_message)

    def successfully_turn_off_mailing_message(self):
        return self._translated_(super().successfully_turn_off_mailing_message)

    def unmute_mailing_mode_question_message(self):
        return self._translated_(super().unmute_mailing_mode_question_message)

    def mute_mailing_mode_question_message(self):
        return self._translated_(super().mute_mailing_mode_question_message)

    def change_mailing_time_question_message(self):
        return self._translated_(super().change_mailing_time_question_message)

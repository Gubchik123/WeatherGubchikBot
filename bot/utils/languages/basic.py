class _Basic:
    """Basic class for extending by other language classes"""

    lang_code: str  # ISO language name (two-letter codes)

    @staticmethod
    def _get_correct_text_from_(string: str) -> str:
        """For getting correct string for message or button text"""
        return string.replace("        ", "")

    def hello_message(self, name: str) -> str:
        """For getting the greeting message text for the 'start' command"""

    def goodbye_message(self, name: str) -> str:
        """For getting the goodbye message text for the 'goodbye' command"""

    def general_rules(self) -> str:
        """For getting the message text with
        general rules of using  for the 'help' command"""

    def searching_message(self) -> str:
        """For getting the searching message text"""

    def wait_message(self) -> str:
        """For getting the waiting message text"""

    def yes_btn(self) -> str:
        """For getting the agree button text"""

    def no_btn(self) -> str:
        """For getting the decline button text"""

    def weather_in_Ukraine_btn(self) -> str:
        """For getting the button text for getting weather in Ukraine"""

    def weather_in_Europe_btn(self) -> str:
        """For getting the button text for getting weather in Europe"""

    def back_to_menu_btn(self) -> str:
        """For getting the returning back button text"""

    def menu_btn_mailing_management(self) -> str:
        """For getting the button text for mailing menu"""

    def menu_btn_turn_on_mailing(self) -> str:
        """For getting the button text for turning on mailing"""

    def menu_btn_goodbye(self) -> str:
        """For getting the goodbye button text"""

    def menu_message(self) -> str:
        """For getting the menu message text"""

    def choose_region_message(self) -> str:
        """For getting the choosing region message text"""

    def repeat_choosing_btn(self) -> str:
        """For getting the repeat button text"""

    def choose_minded_option(self) -> str:
        """For getting the message text for asking about needed variant"""

    def there_are_not_such_type_of_region_message(self) -> str:
        """For getting the message text that there are not such region"""

    def today_btn(self) -> str:
        """For getting the today button text"""

    def tomorrow_btn(self) -> str:
        """For getting the tomorrow button text"""

    def week_btn(self) -> str:
        """For getting the week button text"""

    def two_week_btn(self) -> str:
        """For getting the fortnight button text"""

    def choose_period_message(self) -> str:
        """For getting the choosing period message text"""

    def there_are_not_such_type_of_period_message(self) -> str:
        """For getting the message text that there are not such period"""

    def error_message(self) -> str:
        """For getting the error message text"""
        
    def try_again_message(self) -> str:
        """For getting the message text to try again"""

    def mailing_info_message(
        self, time_int: int, mute: bool, time: str, city: str
    ) -> str:
        """For getting the message text about user's mailing info"""

    def mute_mode_btn(self) -> str:
        """For getting the mute mode button text"""

    def unmute_mode_btn(self) -> str:
        """For getting the unmute mode button text"""

    def change_mailing_time_btn(self) -> str:
        """For getting the changing mailing time button text"""

    def change_mailing_city_btn(self) -> str:
        """For getting the changing mailing city button text"""

    def change_mailing_period_btn(self) -> str:
        """For getting the changing mailing period button text"""

    def turn_off_mailing_btn(self) -> str:
        """For getting the turning off mailing button text"""

    def daily_mailing_message(self) -> str:
        """For getting the mailing message text"""

    def what_do_you_want_to_do_with_mailing_message(self) -> str:
        """For getting the message text for asking about mailing action"""

    def turn_on_mailing_question_message(self) -> str:
        """For getting the message text for asking about turning on mailing"""

    def turn_off_mailing_question_message(self) -> str:
        """For getting the message text for asking turning off mailing"""

    def change_mailing_city_question_message(self) -> str:
        """For getting the message text for asking about changing mailing city"""

    def change_mailing_period_question_message(self) -> str:
        """For getting the message text for asking about changing mailing period"""

    def what_mailing_time_question_message(self) -> str:
        """For getting the message text for asking about mailing time"""

    def mailing_mute_mode_question_message(self) -> str:
        """For getting the message text for asking about mailing mute mode"""

    def ok_action_canceled_message(self) -> str:
        """For getting the cancel message text"""

    def there_are_not_such_type_of_answer_message(self) -> str:
        return "Такої відповіді немає, перевірте та спробуйте ще раз"

    def choose_weather_country_question_message(self) -> str:
        """For getting the message text for asking about choosing weather country"""

    def choose_mailing_country_question_message(self) -> str:
        """For getting the message text for asking about choosing mailing country"""

    def successfully_turn_on_mailing_message(self) -> str:
        """For getting the message text about success turing on mailing"""

    def successfully_turn_off_mailing_message(self) -> str:
        """For getting the message text about success turing off mailing"""

    def unmute_mailing_mode_question_message(self) -> str:
        """For getting the message text for asking about unmute mailing mode"""

    def mute_mailing_mode_question_message(self) -> str:
        """For getting the message text for asking about mute mailing mode"""

    def change_mailing_time_question_message(self) -> str:
        """For getting the message text for asking about changing mailing time"""

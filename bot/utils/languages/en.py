from .basic import _Basic


class EN(_Basic):
    """English language class"""

    lang_code = "en"

    def hello_message(self, name: str) -> str:
        return self._get_correct_text_from_(
            f"""
        Hello, {name}
        I am the one who will help you find out information about the weather in the cities of Ukraine and Europe
        """
        )

    def goodbye_message(self, name: str) -> str:
        return self._get_correct_text_from_(
            f"""
        Bye, {name}, come back again
        Next time just type or press /start :)
        """
        )

    def general_rules(self) -> str:
        return self._get_correct_text_from_(
            """
        Bot commands:
        /start - Start working with the bot
        /language - Change the language of the bot
        /help - Display of basic usage rules
        /weather - Display information about the weather
        /goodbye - Ending work with the bot

        Sign up for the newsletter to receive daily weather information in the city of your choice (you can turn it off at any time)

        I advise you to use the buttons for the intended result

        Enjoy using!!!

        Bot author contacts:
        Instagram: https://www.instagram.com/nikitos.1746/
        GitHub: https://github.com/Gubchik123
        """
        )

    def searching_message(self) -> str:
        return "Searching..."

    def wait_message(self) -> str:
        return "Processing..."

    def yes_btn(self) -> str:
        return "Yes"

    def no_btn(self) -> str:
        return "No"

    def weather_in_Ukraine_btn(self) -> str:
        return "Weather in Ukraine"

    def weather_in_Europe_btn(self) -> str:
        return "Weather in Europe"

    def back_to_menu_btn(self) -> str:
        return "← Return to the main menu"

    def menu_btn_mailing_management(self) -> str:
        return "Mailing management"

    def menu_btn_turn_on_mailing(self) -> str:
        return "Enable mailing"

    def menu_btn_goodbye(self) -> str:
        return "End communication"

    def menu_message(self) -> str:
        return self._get_correct_text_from_(
            """
        You are in the main menu
        Select further actions
        """
        )

    def choose_region_message(self) -> str:
        return "Enter the name of the city / locality"

    def repeat_choosing_btn(self) -> str:
        return "Retry the input"

    def choose_minded_option(self) -> str:
        return "Choose the option you had in mind"

    def there_are_not_such_type_of_region_message(self) -> str:
        return "You chose the wrong option"

    def today_btn(self) -> str:
        return "Today"

    def tomorrow_btn(self) -> str:
        return "Tomorrow"

    def week_btn(self) -> str:
        return "Week"

    def two_week_btn(self) -> str:
        return "Fortnight"

    def choose_period_message(self) -> str:
        return "Select the forecast period"

    def there_are_not_such_type_of_period_message(self) -> str:
        return "Unknown forecast period"

    def error_message(self) -> str:
        return self._get_correct_text_from_(
            """
        An error occurred!
        Please try again or restart the bot with the /start command
        """
        )

    def mailing_info_message(
        self, time_int: int, mute: bool, time: str, city: str
    ) -> str:
        return self._get_correct_text_from_(
            f"""
        You are in the mailing list management menu
        Details of your newsletter:

        Daily at {time_int}:00
        Mode: {'Silent' if mute else 'Alert'}

        Forecast period: {time}
        City / locality: {city}
        """
        )

    def mute_mode_btn(self) -> str:
        return "Enable silent mode"

    def unmute_mode_btn(self) -> str:
        return "Enable notification mode"

    def change_mailing_time_btn(self) -> str:
        return "Change the mailing time"

    def change_mailing_city_btn(self) -> str:
        return "Change city"

    def change_mailing_period_btn(self) -> str:
        return "Change the forecast period"

    def turn_off_mailing_btn(self) -> str:
        return "Turn off mailing"

    def daily_mailing_message(self) -> str:
        return "Daily newsletter"

    def what_do_you_want_to_do_with_mailing_message(self) -> str:
        return "What do you want to do?"

    def turn_on_mailing_question_message(self) -> str:
        return "Do you really want to sign up for a daily weather forecast newsletter?"

    def turn_off_mailing_question_message(self) -> str:
        return "Are you sure you want to cancel your daily weather newsletter?"

    def change_mailing_city_question_message(self) -> str:
        return "Do you really want to change the city?"

    def change_mailing_period_question_message(self) -> str:
        return "Are you sure you want to change the forecast period?"

    def what_mailing_time_question_message(self) -> str:
        return "At what time would you like to receive the newsletter?"

    def mailing_mute_mode_question_message(self) -> str:
        return "Would you like to receive a silent message?"

    def ok_action_canceled_message(self) -> str:
        return "OK, action cancelled"

    def there_are_not_such_type_of_answer_message(self) -> str:
        return "There is no such answer, please check and try again"

    def choose_weather_country_question_message(self) -> str:
        return "Where would you like to see the weather?"

    def choose_mailing_country_question_message(self) -> str:
        return "Where do you want to get the weather?"

    def successfully_turn_on_mailing_message(self) -> str:
        return "You have successfully completed the mailing"

    def successfully_turn_off_mailing_message(self) -> str:
        return "You have successfully canceled your daily weather forecast newsletter"

    def unmute_mailing_mode_question_message(self) -> str:
        return "Are you sure you want to enable notification mode?"

    def mute_mailing_mode_question_message(self) -> str:
        return "Are you sure you want to enable silent mode?"

    def change_mailing_time_question_message(self) -> str:
        return "Are you sure you want to change the delivery time?"

from .basic import _Basic


class UA(_Basic):
    """Ukrainian language class"""

    lang_code = "ua"

    def hello_message(self, name: str) -> str:
        return self._get_correct_text_from_(
            f"""
        Привіт, {name}
        Я той, хто допоможе тобі дізнатись інформацію про погоду в містах України і Європи
        """
        )

    def goodbye_message(self, name: str) -> str:
        return self._get_correct_text_from_(
            f"""
        Бувай, {name}, повертайся ще
        Наступного разу просто введи або натисни /start :)
        """
        )

    def general_rules(self) -> str:
        return self._get_correct_text_from_(
            """
        Команди бота:
        /start - Початок роботи з ботом
        /language - Змінення мови бота
        /help - Відображення основних правил використання
        /weather - Відображення інформації про погоду
        /goodbye - Завершення роботи з ботом

        Оформіть розсилку, щоб кожного дня дізнаватися інформацію про погоду в місті, яке ви обирете (в будь-який час її можно відключити)

        Раджу використати кнопки для задуманого результату

        Приємного використання!!!

        Контакти автора бота:
        CV site: https://nikita-hubariev.me
        LinkedIn: https://www.linkedin.com/in/nikita-hubariev
        Instagram: https://www.instagram.com/nikitos.1746

        Інші проекти автора доступні на:
        Дошка проектів: https://gubchik123-project-board.netlify.app
        GitHub: https://github.com/Gubchik123
        """
        )

    def searching_message(self) -> str:
        return "Пошук..."

    def wait_message(self) -> str:
        return "Опрацювання..."

    def yes_btn(self) -> str:
        return "Так"

    def no_btn(self) -> str:
        return "Ні"

    def weather_in_Ukraine_btn(self) -> str:
        return "Погода в Україні"

    def weather_in_Europe_btn(self) -> str:
        return "Погода в Європі"

    def back_to_menu_btn(self) -> str:
        return "← Повернутися у головне меню"

    def menu_btn_mailing_management(self) -> str:
        return "Управління розсилкою"

    def menu_btn_turn_on_mailing(self) -> str:
        return "Увімкнути розсилку"

    def menu_btn_goodbye(self) -> str:
        return "Закінчити спілкування"

    def menu_message(self) -> str:
        return self._get_correct_text_from_(
            """
        Ви в головному меню
        Виберіть подальші дії
        """
        )

    def choose_region_message(self) -> str:
        return "Введіть назву міста / населеного пункту"

    def repeat_choosing_btn(self) -> str:
        return "Повторити спробу введення"

    def choose_minded_option(self) -> str:
        return "Оберіть варіант, який ви мали на увазі"

    def there_are_not_such_type_of_region_message(self) -> str:
        return "Ви обрали не той варіант"

    def today_btn(self) -> str:
        return "Сьогодні"

    def tomorrow_btn(self) -> str:
        return "Завтра"

    def week_btn(self) -> str:
        return "Тиждень"

    def two_week_btn(self) -> str:
        return "Два тижні"

    def choose_period_message(self) -> str:
        return "Виберіть період прогнозу"

    def there_are_not_such_type_of_period_message(self) -> str:
        return "Невідомий період прогнозу"

    def error_message(self) -> str:
        return "Виникла помилка!"

    def try_again_message(self) -> str:
        return self._get_correct_text_from_(
            f"""
        {self.error_message()}
        Спробуйте повторити спробу або перезапустіть бота командою /start
        """
        )

    def mailing_info_message(
        self, time_int: int, mute: bool, time: str, city: str
    ) -> str:
        return self._get_correct_text_from_(
            f"""
        Ви в меню управління розсилкою
        Деталі вашої розсилки:

        Щодня о {time_int}:00
        Режим: {'Беззвучний' if mute else 'Оповіщення'}

        Період прогнозу: {time}
        Місто / населений пункт: {city}
        """
        )

    def mute_mode_btn(self) -> str:
        return "Увімкнути беззвучний режим"

    def unmute_mode_btn(self) -> str:
        return "Увімкнути режим оповіщення"

    def change_mailing_time_btn(self) -> str:
        return "Змінити час розсилки"

    def change_mailing_city_btn(self) -> str:
        return "Змінити місто"

    def change_mailing_period_btn(self) -> str:
        return "Змінити період прогнозу"

    def turn_off_mailing_btn(self) -> str:
        return "Вимкнути розсилку"

    def daily_mailing_message(self) -> str:
        return "Щоденна розсилка"

    def what_do_you_want_to_do_with_mailing_message(self) -> str:
        return "Що ви бажаєте зробити?"

    def turn_on_mailing_question_message(self) -> str:
        return "Ви дійсно хочете оформити щоденну розсилку прогноза погоди?"

    def turn_off_mailing_question_message(self) -> str:
        return "Ви дійсно хочете відмінити щоденну розсилку прогноза погоди?"

    def change_mailing_city_question_message(self) -> str:
        return "Ви дійсно хочете змінити місто?"

    def change_mailing_period_question_message(self) -> str:
        return "Ви дійсно хочете змінити період прогнозу?"

    def what_mailing_time_question_message(self) -> str:
        return "О котрій годині ви бажаєте отримувати розсилку?"

    def mailing_mute_mode_question_message(self) -> str:
        return "Ви бажаєте отримувати беззвучне повідомлення?"

    def ok_action_canceled_message(self) -> str:
        return "Добре, дії скасовано"

    def there_are_not_such_type_of_answer_message(self) -> str:
        return "Такої відповіді немає, перевірте та спробуйте ще раз"

    def choose_weather_country_question_message(self) -> str:
        return "Де ви бажаєте подивитися погоду?"

    def choose_mailing_country_question_message(self) -> str:
        return "Де ви бажаєте отримувати погоду?"

    def successfully_turn_on_mailing_message(self) -> str:
        return "Ви успішно оформили розсилку"

    def successfully_turn_off_mailing_message(self) -> str:
        return "Ви успішно відмінили щоденну розсилку прогноза погоди"

    def unmute_mailing_mode_question_message(self) -> str:
        return "Ви дійсно хочете увімкнути режим оповіщення?"

    def mute_mailing_mode_question_message(self) -> str:
        return "Ви дійсно хочете увімкнути беззвучний режим?"

    def change_mailing_time_question_message(self) -> str:
        return "Ви дійсно хочете змінити час розсилки?"

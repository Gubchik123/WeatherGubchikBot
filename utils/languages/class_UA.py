class UA:
    def __init__(self, lang_code: str):
        self.lang_code = lang_code

    @staticmethod
    def _get_correct_text_from_(
        string: str): return string.replace("        ", '')

    def hello_message(self, name: str):
        return self._get_correct_text_from_(f"""
        Привіт, {name}
        Я той, хто допоможе тобі дізнатись інформацію про погоду в містах України і Європи
        """)

    def goodbye_message(self, name: str):
        return self._get_correct_text_from_(f"""
        Бувай, {name}, повертайся ще
        Наступного разу просто введи або натисни /start :)
        """)

    def general_rules(self):
        return self._get_correct_text_from_("""
        Команди бота:
        /start - початок роботи з ботом
        /help - основні правила використання
        /weather - відображення інформації про погоду
        /moon - відображення інформації про фазу місяця
        /goodbye - кінець роботи з ботом

        Оформіть розсилку, щоб кожного дня дізнаватися інформацію про погоду в місті, яке ви обирете (в будь-який час її можно відключити)

        Раджу використати кнопки для задуманого результату

        Приємного використання!!!
        """)

    def yes_btn(self): return "Так"

    def no_btn(self): return "Ні"

    def weather_in_Ukraine_btn(self): return "Погода в Україні"

    def weather_in_Europe_btn(self): return "Погода в Європі"

    def back_to_menu_btn(self): return "← Повернутися у головне меню"

    def menu_btn_mailing_managment(self): return "Управління розсилкою"

    def menu_btn_turn_on_mailing(self): return "Увімкнути розсилку"

    def menu_btn_goodbye(self): return "Закінчити спілкування"

    def menu_message(self):
        return self._get_correct_text_from_("""
        Ви в головному меню
        Виберіть подальші дії
        """)

    def choose_region_message(self):
        return "Введіть назву міста / населеного пункту"

    def repeat_choosing_btn(self): return "Повторити спробу введення"

    def choose_minded_option(self):
        return "Оберіть варіант, який ви мали на увазі"

    def there_are_not_such_type_of_region_message(self):
        return "Ви обрали не той варіант"

    def today_btn(self): return "Сьогодні"
    def tomorrow_btn(self): return "Завтра"
    def week_btn(self): return "Тиждень"
    def two_week_btn(self): return "Два тижні"

    def choose_period_message(self): return "Виберіть період прогнозу"

    def there_are_not_such_type_of_period_message(self):
        return "Невідомий період прогнозу"

    def error_message(self):
        return self._get_correct_text_from_("""
        Виникла помилка!
        Спробуйте повторити спробу або перезапустіть бота командою /start
        """)

    def mute_mode_btn(self): return "Увімкнути беззвучний режим"
    def unmute_mode_btn(self): return "Увімкнути режим оповіщення"

    def change_mailing_time_btn(self): return "Змінити час розсилки"
    def change_mailing_city_btn(self): return "Змінити місто"
    def change_mailing_period_btn(self): return "Змінити період прогнозу"
    def turn_off_mailing_btn(self): return "Вимкнути розсилку"

    def daily_mailing_message(self): return "Щоденна розсилка"

    def what_do_you_want_to_do_with_mailing_message(self):
        return "Що ви бажаєте зробити?"

    def turn_on_mailing_question_message(self):
        return "Ви дійсно хочете оформити щоденну розсилку прогноза погоди?"

    def turn_off_mailing_question_message(self):
        return "Ви дійсно хочете відмінити щоденну розсилку прогноза погоди?"

    def change_mailing_city_question_message(self):
        return "Ви дійсно хочете змінити місто?"

    def change_mailing_period_question_message(self):
        return "Ви дійсно хочете змінити період прогнозу?"

    def what_mailing_time_question_message(self):
        return "О котрій годині ви бажаєте отримувати розсилку?"

    def mailing_mute_mode_question_message(self):
        return "Ви бажаєте отримувати беззвучне повідомлення?"

    def ok_action_canceled_message(self): return "Добре, дії скасовано"

    def there_are_not_such_type_of_answer_message(self):
        return "Такої відповіді немає, перевірте та спробуйте ще раз"

    def choose_weather_country_question_message(self):
        return "Де ви бажаєте подивитися погоду?"

    def choose_mailing_country_question_message(self):
        return "Де ви бажаєте отримувати погоду?"

    def successfully_turn_on_mailing_message(self):
        return "Ви успішно оформили розсилку"

    def successfully_turn_off_mailing_message(self):
        return "Ви успішно відмінили щоденну розсилку прогноза погоди"

    def unmute_mailing_mode_question_message(self):
        return "Ви дійсно хочете увімкнути режим оповіщення?"

    def mute_mailing_mode_question_message(self):
        return "Ви дійсно хочете увімкнути беззвучний режим?"

    def change_mailing_time_question_message(self):
        return "Ви дійсно хочете змінити час розсилки?"

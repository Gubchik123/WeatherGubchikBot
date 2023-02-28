from .basic import _Basic


class RU(_Basic):
    """Russian language class"""

    lang_code = "ru"

    def hello_message(self, name: str) -> str:
        return self._get_correct_text_from_(
            f"""
        Привет, {name}
        Я тот, кто поможет тебе узнать информацию о погоде в городах Украины и Европы.
        """
        )

    def goodbye_message(self, name: str) -> str:
        return self._get_correct_text_from_(
            f"""
        Прощай, {name}, возвращайся еще
        В следующий раз просто введи или нажми /start:)
        """
        )

    def general_rules(self) -> str:
        return self._get_correct_text_from_(
            """
        Команды бота:
        /start - Начало работы с ботом
        /language - Изменение языка бота
        /help - Отображение основных правил использования
        /weather - Отображение информации о погоде
        /goodbye - Завершение работы с ботом

        Оформите рассылку, чтобы каждый день узнавать информацию о погоде в выбранном городе (в любое время ее можно отключить)

        Советую использовать кнопки для задуманного результата

        Приятного использования!!!

        Контакты автора бота:
        Instagram: https://www.instagram.com/nikitos.1746/
        GitHub: https://github.com/Gubchik123
        """
        )

    def searching_message(self) -> str:
        return "Поиск..."

    def wait_message(self) -> str:
        return "Обработка..."

    def yes_btn(self) -> str:
        return "Да"

    def no_btn(self) -> str:
        return "Нет"

    def weather_in_Ukraine_btn(self) -> str:
        return "Погода в Украине"

    def weather_in_Europe_btn(self) -> str:
        return "Погода в Европе"

    def back_to_menu_btn(self) -> str:
        return "← Вернуться в главное меню"

    def menu_btn_mailing_management(self) -> str:
        return "Управление рассылкой"

    def menu_btn_turn_on_mailing(self) -> str:
        return "Включить рассылку"

    def menu_btn_goodbye(self) -> str:
        return "Закончить общение"

    def menu_message(self) -> str:
        return self._get_correct_text_from_(
            """
        Вы в главном меню
        Выберите следующие действия
        """
        )

    def choose_region_message(self) -> str:
        return "Введите название города/населенного пункта"

    def repeat_choosing_btn(self) -> str:
        return "Повторить попытку ввода"

    def choose_minded_option(self) -> str:
        return "Выберите вариант, который вы имели в виду"

    def there_are_not_such_type_of_region_message(self) -> str:
        return "Вы выбрали не тот вариант"

    def today_btn(self) -> str:
        return "Сегодня"

    def tomorrow_btn(self) -> str:
        return "Завтра"

    def week_btn(self) -> str:
        return "Неделя"

    def two_week_btn(self) -> str:
        return "Две недели"

    def choose_period_message(self) -> str:
        return "Виберите период прогноза"

    def there_are_not_such_type_of_period_message(self) -> str:
        return "Неизвестный период прогноза"

    def error_message(self) -> str:
        return "Возникла ошибка!"

    def try_again_message(self) -> str:
        return self._get_correct_text_from_(
            f"""
        {self.error_message()}
        Попытайтесь повторить попытку или перезапустите бота командой /start
        """
        )

    def mailing_info_message(
        self, time_int: int, mute: bool, time: str, city: str
    ) -> str:
        return self._get_correct_text_from_(
            f"""
        Вы в меню управления рассылкой
        Детали вашей рассылки:

        Ежедневно в {time_int}:00
        Режим: {'Беззвучный' if mute else 'Уведомление'}

        Период прогноза: {time}
        Город / населенный пункт: {city}
        """
        )

    def mute_mode_btn(self) -> str:
        return "Включить беззвучный режим"

    def unmute_mode_btn(self) -> str:
        return "Включить режим оповещения"

    def change_mailing_time_btn(self) -> str:
        return "Сменить время рассылки"

    def change_mailing_city_btn(self) -> str:
        return "Сменить город"

    def change_mailing_period_btn(self) -> str:
        return "Изменить период прогноза"

    def turn_off_mailing_btn(self) -> str:
        return "Отключить рассылку"

    def daily_mailing_message(self) -> str:
        return "Ежедневная рассылка"

    def what_do_you_want_to_do_with_mailing_message(self) -> str:
        return "Что вы хотите сделать?"

    def turn_on_mailing_question_message(self) -> str:
        return "Вы действительно хотите оформить ежедневную рассылку прогноза погоды?"

    def turn_off_mailing_question_message(self) -> str:
        return "Вы действительно хотите отменить ежедневную рассылку прогноза погоды?"

    def change_mailing_city_question_message(self) -> str:
        return "Вы действительно хотите изменить город?"

    def change_mailing_period_question_message(self) -> str:
        return "Вы действительно хотите изменить период прогноза?"

    def what_mailing_time_question_message(self) -> str:
        return "В какое время вы хотите получать рассылку?"

    def mailing_mute_mode_question_message(self) -> str:
        return "Хотите получать беззвучное сообщение?"

    def ok_action_canceled_message(self) -> str:
        return "Хорошо, действия отменены"

    def there_are_not_such_type_of_answer_message(self) -> str:
        return "Такого ответа нет, перепроверьте и попробуйте еще раз"

    def choose_weather_country_question_message(self) -> str:
        return "Где вы хотите посмотреть погоду?"

    def choose_mailing_country_question_message(self) -> str:
        return "Где вы хотите получать погоду?"

    def successfully_turn_on_mailing_message(self) -> str:
        return "Вы успешно оформили рассылку"

    def successfully_turn_off_mailing_message(self) -> str:
        return "Вы успешно отменили ежедневную рассылку прогноза погоды."

    def unmute_mailing_mode_question_message(self) -> str:
        return "Вы действительно хотите включить режим оповещения?"

    def mute_mailing_mode_question_message(self) -> str:
        return "Вы действительно хотите включить беззвучный режим?"

    def change_mailing_time_question_message(self) -> str:
        return "Вы действительно хотите изменить время рассылки?"

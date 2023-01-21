import logging
from typing import NamedTuple, Callable

import psycopg2

from data import DB_URI
from utils.class_User import TelegramUser
from utils.class_SelectedInfo import SelectedInfo


class UserDBInfo(NamedTuple):
    chat_id: int
    mute: bool
    city: str
    time_title: str
    time: str
    type: str
    time_int: int
    city_title: str
    lang: str


class DB:
    """For working with database"""

    def __init__(self):
        """For initializing some start private variables"""
        self._set_db_connection()

        self.__chat_IDs = self._get_all_chat_IDs()
        self.__rows_for_selecting = """
            chat_id, mute, city, time_title, time, type, time_int, city_title, lang
        """

    @property
    def chat_IDs(self) -> tuple:
        """Getter for users' chat IDs"""
        return self.__chat_IDs

    def catch_closed_connection(func: Callable):
        """Decorator for catching exception by closed connection to db"""

        def inner(self, *args, **kwargs):
            try:
                if not self.__connection:
                    self._set_db_connection()

                return func(self, *args, **kwargs)
            except psycopg2.InterfaceError as e:
                logger = logging.getLogger("my_logger")
                logger.error(f"InterfaceError in db: {str(e)}")

                self._set_db_connection()
                return func(self, *args, **kwargs)

        return inner

    @catch_closed_connection
    def add_(self, user: TelegramUser, info: SelectedInfo):
        """For adding user for mailing in database"""
        with self.__connection.cursor() as cursor:
            sql_adding_query = f"""
                INSERT INTO mailing
                (chat_id, mute, name, 
                city, time, time_title, type, 
                time_int, city_title, lang)
                VALUES
                ({user.chat_id}, {user.selected_mute_mode}, '{user.name}', 
                '{info.city}', '{info.time}', '{info.time_title}', '{info.type}',
                {user.selected_time}, '{info.city_title}', '{info.lang}');
            """
            cursor.execute(sql_adding_query)
        self.__chat_IDs = self._get_all_chat_IDs()

    @catch_closed_connection
    def get_all_users(self) -> tuple:
        """For getting information about users for mailing from database"""
        with self.__connection.cursor() as cursor:
            cursor.execute(f"SELECT {self.__rows_for_selecting} FROM mailing;")
            data = cursor.fetchall()
        return tuple(UserDBInfo(*row) for row in data)

    @catch_closed_connection
    def get_user_with_(self, chat_id: int) -> UserDBInfo:
        """For getting information about user from database by chat id"""
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {self.__rows_for_selecting} FROM mailing WHERE chat_id={chat_id};"
            )
            data = cursor.fetchone()
        return UserDBInfo(*data)

    @catch_closed_connection
    def get_columns_for_user_with_(self, chat_id: int, columns: str) -> tuple:
        """For getting <column> from the database for the user identified by <chat_id>"""
        with self.__connection.cursor() as cursor:
            cursor.execute(f"SELECT {columns} FROM mailing WHERE chat_id={chat_id};")
            data = cursor.fetchone()
        return data

    @catch_closed_connection
    def update_mailing_city_for_user_with_(self, chat_id: int, new_city: dict) -> None:
        """For updating user mailing city in database"""
        with self.__connection.cursor() as cursor:
            sql_update_query = f"""
                UPDATE mailing SET 
                city = '{new_city["string"]}',
                city_title = '{new_city["title"]}'
                WHERE chat_id = {chat_id};
            """
            cursor.execute(sql_update_query)

    @catch_closed_connection
    def update_mailing_mute_mode_for_user_with_(
        self, chat_id: int, new_mute_mode: bool
    ) -> None:
        """For updating user mailing mute mode in database"""
        with self.__connection.cursor() as cursor:
            sql_update_query = f"""
                UPDATE mailing SET mute = {new_mute_mode} WHERE chat_id = {chat_id};
            """
            cursor.execute(sql_update_query)

    @catch_closed_connection
    def update_mailing_time_for_user_with_(
        self, chat_id: int, info: SelectedInfo
    ) -> None:
        """For updating user mailing time in database"""
        with self.__connection.cursor() as cursor:
            sql_update_query = f"""
                UPDATE mailing SET
                time = '{info.time}',
                time_title = '{info.time_title}',
                type = '{info.type}'
                WHERE chat_id = {chat_id};
            """
            cursor.execute(sql_update_query)

    @catch_closed_connection
    def update_mailing_time_int_for_user_with_(
        self, chat_id: int, new_time_int: str
    ) -> None:
        """For updating user mailing time int in database"""
        with self.__connection.cursor() as cursor:
            sql_update_query = f"""
                UPDATE mailing SET time_int = {new_time_int} WHERE chat_id = {chat_id};
            """
            cursor.execute(sql_update_query)

    @catch_closed_connection
    def update_mailing_lang_code_for_user_with_(
        self, chat_id: int, new_lang_code: str
    ) -> None:
        """For checking and updating user mailing language code in database if needed"""
        with self.__connection.cursor() as cursor:
            sql_update_query = f"""
                UPDATE mailing SET lang = '{new_lang_code}' WHERE chat_id = {chat_id};
            """
            cursor.execute(sql_update_query)

    @catch_closed_connection
    def update_last_city_for_user_with_(
        self, chat_id: int, city_type: str, new_last_city: str
    ) -> None:
        """For updating the user's last <Ukrainian or foreign> city, which the user searched"""
        with self.__connection.cursor() as cursor:
            sql_update_query = f"""
                UPDATE mailing SET last_{city_type}_city = '{new_last_city}' 
                WHERE chat_id = {chat_id};
            """
            cursor.execute(sql_update_query)

    @catch_closed_connection
    def delete_user_with_(self, chat_id: int) -> None:
        """For deleting user from database"""
        with self.__connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM mailing WHERE chat_id = {chat_id};")
        self.__chat_IDs = self._get_all_chat_IDs()

    @catch_closed_connection
    def _get_all_chat_IDs(self):
        """For getting all users' chat IDs"""
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT chat_id FROM mailing;")
            data = cursor.fetchall()
        return tuple(row[0] for row in data)

    def _set_db_connection(self) -> None:
        """For setting database connection"""
        self.__connection = psycopg2.connect(DB_URI)
        self.__connection.autocommit = True

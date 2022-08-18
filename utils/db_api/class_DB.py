import psycopg2

from data import DB_URI
from utils.class_User import TelegramUser


class DB:
    def __init__(self):
        self._connection = psycopg2.connect(DB_URI)
        self._connection.autocommit = True

        self.__chat_IDs = self._get_chat_IDs()

    @property  # Getter for list of users' chat IDs
    def chat_IDs(self): return self.__chat_IDs

    def get_information_for_mailing(self) -> tuple:
        """Method for returning information for mailing from database"""
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT chat_id, mute, city FROM mailing;")
            data = cursor.fetchall()
        return data

    def add(self, user: TelegramUser):
        """Method for adding user for mailing in database  and updating list of chat IDs"""
        with self._connection.cursor() as cursor:
            sql_adding_query = f"""
            INSERT INTO mailing
            (chat_id, mute, nik, name, city)
            VALUES
            ({user.chat_id}, {user.selected_mute_mode}, '{user.nik}', '{user.name}', 
            '{user.selected_city}');
            """
            cursor.execute(sql_adding_query)
        self.__chat_IDs = self._get_chat_IDs()

    def delete_user_with(self, chat_id: int):
        """Method for deleting user from database and updating list of chat IDs"""
        with self._connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM mailing WHERE chat_id = {chat_id};")
        self.__chat_IDs = self._get_chat_IDs()

    def _get_chat_IDs(self) -> list:
        """Method for returning list of users' chat ID from database"""
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT chat_id FROM mailing;")
            chat_IDs = cursor.fetchall()
        return [data[0] for data in chat_IDs]

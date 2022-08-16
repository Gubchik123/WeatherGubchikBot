import psycopg2

from data import DB_URI
from utils.class_User import TelegramUser


class DB:
    def __init__(self):
        self._connection = psycopg2.connect(DB_URI)
        self._connection.autocommit = True

    def get_information_for_mailing(self) -> tuple:
        """Method for returning information for mailing from database"""
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT chat_id, mute, city FROM mailing;")
            data = cursor.fetchall()
        return data

    def get_chat_IDs(self) -> list:
        chat_IDs_tuple = self.get_information_for_mailing()
        chat_IDs_list = [value[0] for value in chat_IDs_tuple]
        return chat_IDs_list

    def add(self, user: TelegramUser):
        """Method for adding user for mailing in database"""
        with self._connection.cursor() as cursor:
            sql_adding_query = f"""
            INSERT INTO mailing
            (chat_id, mute, nik, name, city)
            VALUES
            ({user.chat_id}, {user.mute}, '{user.nik}', '{user.name}', '{user.city}');
            """
            cursor.execute(sql_adding_query)

    def delete_user_with(self, chat_id: int):
        """Method for deleting user from database"""
        with self._connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM mailing WHERE chat_id = {chat_id};")

    def some(self):
        with self._connection.cursor() as cursor:
            sql_query = """
            CREATE TABLE mailing(
                chat_id BIGINT NOT NULL PRIMARY KEY,
                mute BOOLEAN NOT NULL,
                nik VARCHAR NOT NULL,
                name VARCHAR NOT NULL,
                city VARCHAR NOT NULL
            );
            """
            cursor.execute(sql_query)

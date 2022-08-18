import psycopg2

from data import DB_URI
from utils.class_User import TelegramUser


class DB:
    def __init__(self):
        self._connection = psycopg2.connect(DB_URI)
        self._connection.autocommit = True

        self.__chat_IDs: list = self._fill_chat_IDs()
        self.__users_info: dict = self._fill_users_info()

    @property  # Getter for list of users' chat IDs
    def chat_IDs(self): return self.__chat_IDs

    def get_information_for_mailing(self) -> tuple:
        """Method for returning information for mailing from database"""
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT chat_id, mute, city FROM mailing;")
            data = cursor.fetchall()
        return data

    def get_information_about_user_with_(self, chat_id: int) -> dict:
        """Method for returning user's selected mute mode and city"""
        return self.__users_info[chat_id]

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

        self.__chat_IDs = self._fill_chat_IDs()
        self.__users_info[user.chat_id] = {
            "mute": user.selected_mute_mode,
            "city": user.selected_city
        }

    def update_user_with(self, chat_id: int, what_update: str, new_item: str | bool):
        """Method for updating some user's information in from database"""
        with self._connection.cursor() as cursor:
            if what_update == "city":
                sql_update_query = f"""
                UPDATE mailing SET city = '{new_item}' WHERE chat_id = {chat_id}
                """
            elif what_update == "mute":
                sql_update_query = f"""
                UPDATE mailing SET mute = {new_item} WHERE chat_id = {chat_id}
                """
            cursor.execute(sql_update_query)

        self.__users_info[chat_id][what_update] = new_item

    def delete_user_with(self, chat_id: int):
        """Method for deleting user from database and updating list of chat IDs"""
        with self._connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM mailing WHERE chat_id = {chat_id};")

        self.__chat_IDs.remove(chat_id)
        self.__users_info.pop(chat_id)

    def _fill_chat_IDs(self) -> list:
        """Method for returning list of users' chat ID from database"""
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT chat_id FROM mailing;")
            chat_IDs = cursor.fetchall()
        return [data[0] for data in chat_IDs]

    def _fill_users_info(self) -> dict:
        """Method for returning dict of some users' information from database"""
        users_info = self.get_information_for_mailing()

        return {data[0]: {"mute": data[1], "city": data[2]} for data in users_info}

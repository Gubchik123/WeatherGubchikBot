import psycopg2

from data import DB_URI
from utils.class_User import TelegramUser
from utils.class_SelectedInfo import SelectedInfo


class DB:
    """For working with database"""

    def __init__(self):
        """For getting db connection and some start info"""
        self._connection = psycopg2.connect(DB_URI)
        self._connection.autocommit = True

        self.__chat_IDs: list = self._fill_chat_IDs()
        self.__users_info: dict = self._fill_users_info()

    @property
    def chat_IDs(self):
        """Getter for list of users' chat IDs"""
        return self.__chat_IDs

    def get_mailing_information(self) -> list:
        """For returning information for mailing from database"""
        with self._connection.cursor() as cursor:
            cursor.execute(
                """SELECT chat_id, mute, city, time_title, time, 
                type, time_int, city_title, lang FROM mailing;"""
            )
            data = cursor.fetchall()
        return data

    def get_information_about_user_with_(self, chat_id: int) -> dict:
        """For returning user's selected mute mode and city"""
        return self.__users_info[chat_id]

    def add(self, user: TelegramUser, info: SelectedInfo):
        """For adding user for mailing in database  and updating list of chat IDs"""
        with self._connection.cursor() as cursor:
            sql_adding_query = f"""
            INSERT INTO mailing
            (chat_id, mute, name, city, time, time_title, 
            type, time_int, city_title, lang)
            VALUES
            ({user.chat_id}, {user.selected_mute_mode}, '{user.name}', 
            '{info.city}', '{info.time}', '{info.time_title}', '{info.type}',
            {user.selected_time}, '{info.city_title}', '{info.lang}');
            """
            cursor.execute(sql_adding_query)

        self.__chat_IDs.append(user.chat_id)
        self.__users_info[user.chat_id] = {
            "mute": user.selected_mute_mode,
            "city": info.city_title,
            "time": info.time_title,
            "time_int": user.selected_time,
            "lang": info.lang,
        }

    def update_user_with(self, chat_id: int, what_update: str, new_item):
        """For updating some user's information in from database"""
        with self._connection.cursor() as cursor:
            if what_update == "city":
                sql_update_query = f"""
                UPDATE mailing SET 
                city = '{new_item[0]}',
                city_title = '{new_item[1]}'
                WHERE chat_id = {chat_id}
                """

                new_item = new_item[1]
            elif what_update == "mute":
                sql_update_query = f"""
                UPDATE mailing SET mute = {new_item} WHERE chat_id = {chat_id}
                """
            elif what_update == "time":
                sql_update_query = f"""
                UPDATE mailing SET
                time = '{new_item.time}',
                time_title = '{new_item.time_title}',
                type = '{new_item.type}'
                WHERE chat_id = {chat_id}
                """

                new_item = new_item.time_title
            elif what_update == "time_int":
                sql_update_query = f"""
                UPDATE mailing SET time_int = {new_item} WHERE chat_id = {chat_id}
                """
            elif what_update == "lang":
                sql_update_query = f"""
                UPDATE mailing SET lang = '{new_item}' WHERE chat_id = {chat_id}
                """
            cursor.execute(sql_update_query)

        self.__users_info[chat_id][what_update] = new_item

    def update_user_lang_with_(self, chat_id: int, lang: str):
        """For updating user language code in database"""
        data: dict = self.get_information_about_user_with_(chat_id)

        if data["lang"] != lang:
            self.update_user_with(chat_id, what_update="lang", new_item=lang)

    def delete_user_with(self, chat_id: int):
        """For deleting user from database"""
        with self._connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM mailing WHERE chat_id = {chat_id};")

        self.__chat_IDs.remove(chat_id)
        self.__users_info.pop(chat_id)

    def _fill_chat_IDs(self) -> dict:
        """For returning list of users' chat IDs from database"""
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT chat_id FROM mailing;")
            chat_IDs = cursor.fetchall()
        return [data[0] for data in chat_IDs]

    def _fill_users_info(self) -> dict:
        """For returning dict of some users' information from database"""
        users_info = self.get_mailing_information()

        return {
            data[0]: {
                "mute": data[1],
                "city": data[7],
                "time": data[3],
                "time_int": data[6],
                "lang": data[8],
            }
            for data in users_info
        }

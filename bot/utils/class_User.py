from aiogram.types import Message


class TelegramUser:
    """For storing info about user"""

    def __init__(self, message: Message, mute_mode: bool, time: int):
        """For initializing user by information from telegram"""
        self.__name = message.from_user.first_name
        self.__chat_id = message.from_user.id
        self.__mute = mute_mode
        self.__time = time

    @property
    def name(self):
        """Getter for user's name"""
        return self.__name

    @property
    def chat_id(self):
        """Getter for user's chat_id"""
        return self.__chat_id

    @property
    def selected_mute_mode(self):
        """Getter for user's selected mute mode"""
        return self.__mute

    @property
    def selected_time(self):
        """Getter for user's selected time"""
        return self.__time

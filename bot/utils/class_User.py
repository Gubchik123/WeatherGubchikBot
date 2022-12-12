from aiogram.types import Message


class TelegramUser:
    def __init__(self, message: Message, mute_mode: bool, time: int):
        """Constructor for initializing user by information from telegram"""
        self.__name = message.from_user.first_name
        self.__chat_id = message.from_user.id
        self.__mute = mute_mode
        self.__time = time

    @property  # Getter for user's name
    def name(self):
        return self.__name

    @property  # Getter for user's chat_id
    def chat_id(self):
        return self.__chat_id

    @property  # Getter for user's selected mute mode
    def selected_mute_mode(self):
        return self.__mute

    @property  # Getter for user's selected time
    def selected_time(self):
        return self.__time

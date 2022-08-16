from aiogram.types import Message


class TelegramUser:
    def __init__(self, message: Message, mute_mode: bool, city: str):
        """Constructor for inicializing user by information from telegram"""
        self.__nik = message.from_user.username
        self.__name = message.from_user.first_name
        self.__chat_id = message.from_user.id
        self.__mute = mute_mode
        self.__city = city

    @property  # Getter for user's nik
    def nik(self): return self.__nik

    @property  # Getter for user's name
    def name(self): return self.__name

    @property  # Getter for user's chat_id
    def chat_id(self): return self.__chat_id

    @property  # Getter for user's mute mode
    def mute(self): return self.__mute

    @property  # Getter for choosed user's city
    def city(self): return self.__city

from .uk import UK
from .en import EN
from .ru import RU


class Language:
    """To interact with the languages"""

    def __init__(self):
        """For initializing and creating language object"""
        self.__lang_obj = None

    def __call__(self):
        """For getting current language object"""
        return self.__lang_obj

    def change_on(self, lang_code: str):
        """For changing language"""
        self.__lang_obj = (
            UK() if lang_code == "uk" else (RU() if lang_code == "ru" else EN())
        )

    def check_language_by_(self, lang_code: str):
        """For checking language and changing if needed"""
        if not self.__lang_obj or lang_code != self().lang_code:
            self.change_on(lang_code)

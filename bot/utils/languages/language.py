from .uk import UK
from .en import EN
from .ru import RU


class Language:
    def __init__(self):
        self.__lang_obj = None

    def __call__(self):
        return self.__lang_obj

    def change_on(self, lang_code: str):
        self.__lang_obj = (
            UK() if lang_code == "uk" else (RU() if lang_code == "ru" else EN())
        )

    def check_language_by_(self, lang_code: str):
        if not self.__lang_obj or lang_code != self().lang_code:
            self.change_on(lang_code)

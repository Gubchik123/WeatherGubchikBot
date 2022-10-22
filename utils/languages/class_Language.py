from langdetect import detect

from .class_UA import UA
from .class_EN import EN
from .class_RU import RU


class Language:
    def __init__(self):
        self.__lang = None

    def __call__(self):
        return self.__lang

    def change_on(self, lang_code: str):
        self.__lang = UA(lang_code) if lang_code in ["ua", "uk"] else (
            RU(lang_code) if lang_code == "ru" else EN(lang_code)
        )

    def change_on_detected_language_from(self, text: str):
        detected_lang = detect(text)

        if not self.__lang or detected_lang != self().lang_code:
            print("yes")
            self.change_on(detected_lang)

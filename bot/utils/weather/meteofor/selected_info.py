from ..selected_info import BaseSelectedInfo


class SelectedInfo(BaseSelectedInfo):
    """For storing info for weather searching"""

    now = "now"
    today = ""
    tomorrow = "tomorrow"
    week = "weekly"
    fortnight = "2-weeks"

    def set(self, **kwargs) -> None:
        """For cleaning and setting data"""
        super().set(**kwargs)
        self.set_site_domain_by_(self.lang_code)

    def clean_information(self) -> None:
        """For cleaning all data for weather searching"""
        self.city = ""
        self.time = ""
        self.lang_code = ""

    def set_site_domain_by_(self, lang_code: str) -> None:
        """For setting site domain"""
        self.site_domain = {
            "en": "https://meteofor.com",
            "ua": "https://meteofor.com.ua",
            "ru": "https://meteofor.com.ua/ru/",
        }.get(lang_code)

    @property
    def generated_url(self) -> str:
        """Getter for generated url"""
        return f"{self.site_domain}/{self.city}/{self.time}/"

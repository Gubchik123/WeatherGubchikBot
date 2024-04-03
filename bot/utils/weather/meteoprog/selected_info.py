from ..selected_info import BaseSelectedInfo


class SelectedInfo(BaseSelectedInfo):
    """For storing info for weather searching"""

    today = ""
    tomorrow = "tomorrow"
    week = "6_10"
    fortnight = "review"

    def set(self, **kwargs) -> None:
        """For cleaning and setting data"""
        super().set(**kwargs)
        self.time = "" if self.time == "review" else self.time

    def clean_information(self) -> None:
        """For cleaning all data for weather searching"""
        self.lang_code = ""
        self.city = ""
        self.city_title = ""
        self.time = ""
        self.time_title = ""
        self.type = "weather"

    @property
    def generated_url(self) -> str:
        """Getter for generated url"""
        if self.about_big_city:
            return f"https://www.meteoprog.com/{self.lang_code}/{self.type}/{self.city}/{self.time}"
        return (
            f"https://www.meteoprog.com/{self.lang_code}/weather/{self.city}/"
        )

    @property
    def about_big_city(self) -> bool:
        """Getter for condition about big city"""
        return "-" not in self.city

    @property
    def about_fortnight(self) -> bool:
        """Getter for condition about fortnight"""
        return self.type == "review"

class SelectedInfo:
    """For storing info for weather searching"""

    def __init__(self, **kwargs) -> None:
        """For cleaning and initializing data"""
        self.set(**kwargs)

    def set(self, **kwargs) -> None:
        """For cleaning and setting data"""
        self.clean_information()

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._set_time()

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
            return f"https://www.meteoprog.ua/ua/{self.type}/{self.city}/{self.time}"
        return f"https://www.meteoprog.ua/ua/weather/{self.city}/"

    @property
    def about_big_city(self) -> bool:
        """Getter for condition about big city"""
        return "-" not in self.city

    @property
    def about_today(self) -> bool:
        """Getter for condition about today"""
        return self.time == ""

    @property
    def about_tomorrow(self) -> bool:
        """Getter for condition about tomorrow"""
        return self.time == "tomorrow"

    @property
    def about_week(self) -> bool:
        """Getter for condition about week"""
        return self.time == "6_10"

    @property
    def about_fortnight(self) -> bool:
        """Getter for condition about fortnight"""
        return self.type == "review"

    @property
    def about_one_day(self) -> bool:
        """Getter for condition about one day"""
        return self.type == "weather" and (
            self.about_today or self.about_tomorrow
        )

    @property
    def about_many_days(self) -> bool:
        """Getter for condition about many days"""
        return self.about_week or self.about_fortnight

    def _set_time(self) -> str:
        """Sets special time string."""
        if self.time_title in ["сьогодні", "сегодня", "today"]:
            self.time = ""
        elif self.time_title in ["завтра", "tomorrow"]:
            self.time = "tomorrow"
        elif self.time_title in ["тиждень", "неделя", "week"]:
            self.time = "6_10"
        elif self.time_title in ["два тижні", "две недели", "fortnight"]:
            self.type = "review"

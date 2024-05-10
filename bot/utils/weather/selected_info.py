class BaseSelectedInfo:
    """For storing info for weather searching"""

    now: str
    today: str
    tomorrow: str
    week: str
    fortnight: str

    def __init__(self, **kwargs) -> None:
        """For cleaning and initializing data"""
        self.set(**kwargs)

    def set(self, **kwargs) -> None:
        """For cleaning and setting data"""
        self.clean_information()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def clean_information(self) -> None:
        """For cleaning all data for weather searching"""

    @property
    def generated_url(self) -> str:
        """Getter for generated url"""

    @property
    def about_now(self) -> bool:
        """Getter for condition about now"""
        return self.time == self.now

    @property
    def about_today(self) -> bool:
        """Getter for condition about today"""
        return self.time == self.today

    @property
    def about_tomorrow(self) -> bool:
        """Getter for condition about tomorrow"""
        return self.time == self.tomorrow

    @property
    def about_week(self) -> bool:
        """Getter for condition about week"""
        return self.time == self.week

    @property
    def about_fortnight(self) -> bool:
        """Getter for condition about fortnight"""
        return self.time == self.fortnight

    @property
    def about_one_day(self) -> bool:
        """Getter for condition about one day"""
        return self.about_now or self.about_today or self.about_tomorrow

    @property
    def about_many_days(self) -> bool:
        """Getter for condition about many days"""
        return self.about_week or self.about_fortnight

    @classmethod
    def get_time_by_(cls, time_title: str) -> str:
        """Returns special time string by the given time title."""
        if time_title in ("зараз", "сейчас", "now"):
            return cls.now
        elif time_title in ("сьогодні", "сегодня", "today"):
            return cls.today
        elif time_title in ("завтра", "tomorrow"):
            return cls.tomorrow
        elif time_title in ("тиждень", "неделя", "week"):
            return cls.week
        elif time_title in ("два тижні", "две недели", "fortnight"):
            return cls.fortnight

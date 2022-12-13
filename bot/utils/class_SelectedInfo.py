class SelectedInfo:
    """For storing info for weather searching"""

    def __init__(self):
        """For initializing and cleaning data"""
        self.clean_information()

    def clean_information(self):
        """For cleaning all data for weather searching"""
        self.regions = {}
        self.goal = ""
        self.city = ""
        self.city_title = ""
        self.time = ""
        self.time_title = ""
        self.type = "weather"

    @property
    def region_titles(self):
        """Getter for region titles"""
        return self.regions.keys()

    @property
    def generated_url(self):
        """Getter for generated url"""
        return f"https://www.meteoprog.ua/ua/{self.type}/{self.city}/{self.time}"

    @property
    def about_one_day(self):
        """Getter for condition about one day"""
        return self.type == "weather" and self.time == "" or self.time == "tomorrow"

    @property
    def about_many_days(self):
        """Getter for condition about many days"""
        return self.type == "review" or self.time == "6_10"

    @property
    def about_today(self):
        """Getter for condition about today"""
        return self.time == ""

    def get_time(self):
        """For returning special string for time for site link"""
        if self.time_title in ["сьогодні", "сегодня", "today"]:
            return ""

        if self.time_title in ["завтра", "tomorrow"]:
            return "tomorrow"

        if self.time_title in ["тиждень", "неделя", "week"]:
            return "6_10"

        if self.time_title in ["два тижні", "две недели", "fortnight"]:
            return "review"

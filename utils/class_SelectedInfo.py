class SelectedInfo:
    def __init__(self):
        self.clean_information()

    def clean_information(self):
        self.regions = {}
        self.goal = ""
        self.city = ""
        self.city_title = ""
        self.time = ""
        self.time_title = ""
        self.type = "weather"

    @property  # Getter for region titles
    def region_titles(self): return self.regions.keys()

    @property  # Getter for generated url
    def generated_url(self):
        return f"https://www.meteoprog.ua/ua/{self.type}/{self.city}/{self.time}"

    @property  # Getter for condition about one day
    def about_one_day(self):
        return self.type == "weather" and self.time == "" or self.time == "tomorrow"

    @property  # Getter for condition about many days
    def about_many_days(self):
        return self.type == "review" or self.time == "6_10"

    @property  # Getter for condition about today
    def about_today(self):
        return self.time == ""

    def get_time(self):
        """Method for returning special string for time for site link"""
        return {
            "сьогодні": "",
            "завтра": "tomorrow",
            "тиждень": "6_10",
            "два тижні": "review",

            "сегодня": "",
            "завтра": "tomorrow",
            "неделя": "6_10",
            "две недели": "review",

            "today": "",
            "tomorrow": "tomorrow",
            "week": "6_10",
            "fortnight": "review"
        }.get(self.time_title)

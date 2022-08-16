from data.regions_and_cities import REGIONS_AND_CITIES_DICT


class SelectedInfo:
    def __init__(self):
        self.__regions = REGIONS_AND_CITIES_DICT
        self.clean_information()

    def clean_information(self):
        self.__cities = {}
        self.__goal = ""
        self.__city = ""
        self.__time = ""
        self.__type = "weather"

    @property  # Getter for region titles
    def region_titles(self): return self.__regions.keys()

    @property  # Getter for regions dict
    def regions(self): return self.__regions

    @regions.setter  # Setter for regions dict
    def regions(self, item: dict): self.__regions = item

    @property  # Getter for city titles
    def city_titles(self): return self.__cities.keys()

    @property  # Getter for cities dict
    def cities(self): return self.__cities

    @cities.setter  # Setter for cities dict
    def cities(self, item: dict): self.__cities = item

    @property  # Getter for selected goal
    def goal(self): return self.__goal

    @goal.setter  # Setter for selected goal
    def goal(self, item: str): self.__goal = item

    @property  # Getter for selected city
    def city(self): return self.__city

    @city.setter  # Setter for selected city
    def city(self, item: str): self.__city = item

    @property  # Getter for selected time
    def time(self): return self.__time

    @time.setter  # Setter for selected time
    def time(self, item: str): self.__time = item

    @property  # Getter for selected type
    def type(self): return self.__type

    @type.setter  # Setter for selected type
    def type(self, item: str): self.__type = item

    @property  # Getter for generated url
    def generated_url(self):
        return f"https://www.meteoprog.ua/ua/{self.__type}/{self.__city}/{self.__time}"

    @property  # Getter for condition about one day
    def about_one_day(self):
        return self.__type == "weather" and self.__time == "" or self.__time == "tomorrow"

    @property  # Getter for condition about many days
    def about_many_days(self):
        return self.__type == "review" or self.__time == "6_10"

    @property  # Getter for condition about today
    def about_today(self):
        return self.__time == ""

    def get_time_by_(self, name: str):
        return {
            "сьогодні": lambda: "",
            "завтра": lambda: "tomorrow",
            "тиждень": lambda: "6_10",
            "два тижня": lambda: "review"
        }.get(name)()

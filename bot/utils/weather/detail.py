from typing import NamedTuple


class WeatherDetail(NamedTuple):
    """Named tuple for storing weather details after parsing."""

    wind: str
    rain: str
    humidity: str


class WeatherDetailTitle(WeatherDetail):
    """Named tuple for storing weather detail titles by language."""


def get_weather_detail_titles_by_(lang_code: str) -> WeatherDetailTitle:
    """Returns weather detail titles by the given language code."""
    return {
        "ua": WeatherDetailTitle(
            rain="Імовірність опадів", wind="Вітер", humidity="Вологість"
        ),
        "ru": WeatherDetailTitle(
            rain="Возможность осадков", wind="Ветер", humidity="Влажность"
        ),
        "en": WeatherDetailTitle(
            rain="Chance of precipitation", wind="Wind", humidity="Humidity"
        ),
    }.get(lang_code)

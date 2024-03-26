from sqlalchemy.orm import Session

from ..models import WeatherProviderInfo
from ..db import MySession, add_commit_and_refresh


def get_weather_provider_info_by_(
    city: str, time: str, type: str
) -> WeatherProviderInfo:
    """Returns weather provider info by the given city, time, and type."""
    with MySession() as session:
        weather_provider_info = (
            session.query(WeatherProviderInfo)
            .filter(
                WeatherProviderInfo.city == city,
                WeatherProviderInfo.time == time,
                WeatherProviderInfo.type == type,
            )
            .first()
        )
    return weather_provider_info


def get_or_create_weather_provider_info_by_(
    state_data: dict,
) -> WeatherProviderInfo:
    city = state_data["city"]
    time = state_data["time_title"]
    type = "review" if time == "fortnight" else "weather"

    weather_provider_info = get_weather_provider_info_by_(city, time, type)

    if not weather_provider_info:
        weather_provider_info = WeatherProviderInfo(
            city=city, time=time, type=type
        )
        add_commit_and_refresh(weather_provider_info)
    return weather_provider_info

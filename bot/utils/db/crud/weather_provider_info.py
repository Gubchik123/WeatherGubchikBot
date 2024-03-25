from sqlalchemy.orm import Session

from ..db import MySession
from ..models import WeatherProviderInfo


def _get_weather_provider_info_by_(
    session: Session, user_chat_id: int
) -> WeatherProviderInfo:
    """Returns weather provider info by the given session and user chat id."""
    return (
        session.query(WeatherProviderInfo)
        .filter(WeatherProviderInfo.id_mailing_id == user_chat_id)
        .first()
    )


def get_weather_provider_info_by_(user_chat_id: int) -> WeatherProviderInfo:
    """Returns weather provider info by the given user chat id."""
    with MySession() as session:
        weather_provider_info = _get_weather_provider_info_by_(
            session, user_chat_id
        )
    return weather_provider_info

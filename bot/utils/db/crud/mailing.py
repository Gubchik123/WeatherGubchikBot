from typing import Union

from sqlalchemy import update
from sqlalchemy.orm import Session

from ..models import Mailing, WeatherProviderInfo
from ..db import MySession, commit_and_refresh, add_commit_and_refresh

from .weather_provider_info import get_weather_provider_info_by_


def _get_mailing_by_(session: Session, user_chat_id: int) -> Mailing:
    """Returns mailing by the given session and user chat id."""
    return (
        session.query(Mailing)
        .filter(Mailing.id_user_id == user_chat_id)
        .first()
    )


def create_mailing_for_(user_id: int, state_data: dict) -> None:
    """Creates a new mailing."""
    mailing = Mailing(
        id_user_id=user_id,
        mute=state_data["mute"],
        city=state_data["city_title"],
        time_int=state_data["time_int"],
        time_title=state_data["time_title"],
    )
    add_commit_and_refresh(mailing)

    _create_weather_provider_info_for_(mailing, state_data)


def _create_weather_provider_info_for_(
    mailing: Mailing, state_data: dict
) -> None:
    weather_provider_info = get_weather_provider_info_by_(mailing.id_user_id)

    if not weather_provider_info:
        weather_provider_info = WeatherProviderInfo(
            id_mailing_id=mailing.id_user_id,
            city=state_data["city"],
            time=state_data["time_title"],
            type=(
                "review"
                if state_data["time_title"] == "fortnight"
                else "weather"
            ),
        )
        add_commit_and_refresh(weather_provider_info)


def get_mailing_by_(user_chat_id: int) -> Mailing:
    """Returns mailing by the given user chat id."""
    with MySession() as session:
        mailing = _get_mailing_by_(session, user_chat_id)
    return mailing

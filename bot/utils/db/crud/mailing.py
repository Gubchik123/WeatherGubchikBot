from typing import Union

from sqlalchemy import update
from sqlalchemy.orm import Session, joinedload

from ..models import Mailing
from ..db import MySession, commit_and_refresh, add_commit_and_refresh

from .weather_provider_info import get_or_create_weather_provider_info_by_


def create_mailing_for_(user_id: int, state_data: dict) -> None:
    """Creates a new mailing."""
    weather_provider_info = get_or_create_weather_provider_info_by_(state_data)

    mailing = Mailing(
        id_user_id=user_id,
        mute=state_data["mute"],
        city=state_data["city_title"],
        time_int=state_data["time_int"],
        time_title=state_data["time_title"],
        weather_provider_info_id=weather_provider_info.id,
    )
    add_commit_and_refresh(mailing)


def get_mailing_by_(user_chat_id: int) -> Mailing:
    """Returns mailing by the given user chat id."""
    with MySession() as session:
        mailing = (
            session.query(Mailing)
            .filter(Mailing.id_user_id == user_chat_id)
            .first()
        )
    return mailing

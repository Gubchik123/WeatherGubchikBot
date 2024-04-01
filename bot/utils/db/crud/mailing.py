from typing import Dict, Union

from sqlalchemy import update
from sqlalchemy.orm import Session

from ..models import Mailing
from ..db import LocalSession, add_commit_and_refresh

from .weather_provider_info import get_or_create_weather_provider_info_by_


mailings_cache: Dict[int, Mailing] = {}


def create_mailing_for_(user_id: int, state_data: dict) -> None:
    """Creates a new mailing."""
    weather_provider_info = get_or_create_weather_provider_info_by_(state_data)

    add_commit_and_refresh(
        Mailing(
            id_user_id=user_id,
            mute=state_data["mute"],
            city=state_data["city_title"],
            time_int=state_data["time_int"],
            time_title=state_data["time_title"],
            weather_provider_info_id=weather_provider_info.id,
        )
    )


def _get_mailing_by_(
    session: Session, user_chat_id: int
) -> Union[Mailing, None]:
    """Returns mailing by the given session and user chat id."""
    return (
        session.query(Mailing)
        .filter(Mailing.id_user_id == user_chat_id)
        .first()
    )


def get_mailing_by_(user_chat_id: int) -> Union[Mailing, None]:
    """Returns mailing by the given user chat id."""
    if user_chat_id in mailings_cache:
        return mailings_cache[user_chat_id]

    with LocalSession() as session:
        mailing = _get_mailing_by_(session, user_chat_id)
        if mailing is not None:
            mailings_cache[user_chat_id] = mailing
    return mailing


def update_mailing_with_(user_chat_id: int, **fields) -> None:
    """Updates the mailing by the given user chat id with the given fields."""
    with LocalSession() as session:
        session.execute(
            update(Mailing)
            .where(Mailing.id_user_id == user_chat_id)
            .values(**fields)
        )
        session.commit()

    if user_chat_id in mailings_cache:
        for field, value in fields.items():
            setattr(mailings_cache[user_chat_id], field, value)


def update_mailing_period(user_chat_id: int, data: dict) -> None:
    """Updates the period of the mailing for the given user chat id."""
    mailing = get_mailing_by_(user_chat_id)
    data["city"] = mailing.weather_provider_info.city
    weather_provider_info = get_or_create_weather_provider_info_by_(data)

    with LocalSession() as session:
        session.execute(
            update(Mailing)
            .where(Mailing.id_user_id == user_chat_id)
            .values(
                time_title=data["time_title"],
                weather_provider_info_id=weather_provider_info.id,
            )
        )
        session.commit()

    if user_chat_id in mailings_cache:
        del mailings_cache[user_chat_id]  # * to get new weather provider info


def update_mailing_city(user_chat_id: int, city: str, city_title: str) -> None:
    """Updates the city of the mailing for the given user chat id."""
    mailing = get_mailing_by_(user_chat_id)
    weather_provider_info = get_or_create_weather_provider_info_by_(
        {
            "city": city,
            "time": mailing.weather_provider_info.time,
            "type": mailing.weather_provider_info.type,
        }
    )
    with LocalSession() as session:
        session.execute(
            update(Mailing)
            .where(Mailing.id_user_id == user_chat_id)
            .values(
                city=city_title,
                weather_provider_info_id=weather_provider_info.id,
            )
        )
        session.commit()

    if user_chat_id in mailings_cache:
        del mailings_cache[user_chat_id]  # * to get new weather provider info


def delete_mailing_for_(user_chat_id: int) -> None:
    """Deletes the mailing for the given user chat id."""
    with LocalSession() as session:
        mailing = _get_mailing_by_(session, user_chat_id)
        session.delete(mailing)
        session.commit()

    if user_chat_id in mailings_cache:
        del mailings_cache[user_chat_id]

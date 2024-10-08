from datetime import datetime
from typing import Dict, Union, List, Optional

from sqlalchemy import update
from pytz import timezone as tz
from sqlalchemy.orm import Session
from aiogram.types import User as TelegramUser

from data.config import DEFAULT_TIMEZONE

from ..models import User
from ..db import LocalSession, add_commit_and_refresh


users_cache: Dict[int, User] = {}


def _get_user_by_(session: Session, user_chat_id: int) -> Union[User, None]:
    """Returns user by the given session and user chat id."""
    return session.query(User).filter(User.chat_id == user_chat_id).first()


def create_user_by_(telegram_user: TelegramUser, **fields) -> User:
    """Creates user in database by the given telegram user."""
    return add_commit_and_refresh(
        User(
            chat_id=telegram_user.id,
            username=telegram_user.username,
            full_name=telegram_user.full_name,
            weather_provider=fields.pop("weather_provider", "meteoprog"),
            **fields,
            created=datetime.now(tz(DEFAULT_TIMEZONE)),
        )
    )


def get_user_by_(user_chat_id: int) -> Union[User, None]:
    """Returns user by the given user chat id."""
    if user_chat_id in users_cache:
        return users_cache[user_chat_id]

    with LocalSession() as session:
        user = _get_user_by_(session, user_chat_id)
        if user is not None:
            users_cache[user_chat_id] = user
    return user


def get_user_locale_by_(user_chat_id: int) -> Union[str, None]:
    """Returns user language code by the given user chat id."""
    user = get_user_by_(user_chat_id)
    return user.locale if user else None


def get_users(condition: Optional[bool] = User.chat_id > 0) -> List[User]:
    """Returns all users."""
    with LocalSession() as session:
        users = session.query(User).filter(condition).all()
    return users


def get_users_count(condition: Optional[bool] = User.chat_id > 0) -> int:
    """Returns the count of all users."""
    with LocalSession() as session:
        count = session.query(User).filter(condition).count()
    return count


def update_user_with_(user_chat_id: int, **fields) -> None:
    """Updates the user by the given user chat id with the given fields."""
    with LocalSession() as session:
        session.execute(
            update(User).where(User.chat_id == user_chat_id).values(**fields)
        )
        session.commit()

    if user_chat_id in users_cache:
        for field, value in fields.items():
            setattr(users_cache[user_chat_id], field, value)


def delete_user_with_(user_chat_id: int) -> None:
    """Deletes user with the given user chat id."""
    with LocalSession() as session:
        user = _get_user_by_(session, user_chat_id)
        session.delete(user)
        session.commit()

    if user_chat_id in users_cache:
        del users_cache[user_chat_id]

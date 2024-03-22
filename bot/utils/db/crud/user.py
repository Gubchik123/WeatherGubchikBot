from typing import Union

from sqlalchemy import update
from sqlalchemy.orm import Session
from aiogram.types import User as TelegramUser

from ..models import User
from ..db import MySession, commit_and_refresh, add_commit_and_refresh


users = {}


def _get_user_by_(session: Session, user_chat_id: int) -> User:
    """Returns user by the given session and user chat id."""
    return session.query(User).filter(User.chat_id == user_chat_id).first()


def create_user_by_(telegram_user: TelegramUser, message_args: str) -> None:
    """Creates user in database by the given telegram user."""
    add_commit_and_refresh(
        User(
            chat_id=telegram_user.id,
            username=telegram_user.username,
            full_name=telegram_user.full_name,
        )
    )


def get_user_by_(user_chat_id: int) -> User:
    """Returns user by the given user chat id."""
    try:
        if (user := users[user_chat_id]) is None:
            raise KeyError
        return user
    except KeyError:
        with MySession() as session:
            user = _get_user_by_(session, user_chat_id)
        users[user_chat_id] = user
        return user


def get_user_locale_by_(user_chat_id: int) -> Union[str, None]:
    """Returns user language code by the given user chat id."""
    user = get_user_by_(user_chat_id)
    return user.locale if user else None


def change_user_locale_by_(user_chat_id: int, locale: str) -> None:
    """Changes user language by the given user chat id and language code."""
    with MySession() as session:
        session.execute(
            update(User)
            .where(User.chat_id == user_chat_id)
            .values(locale=locale)
        )
        session.commit()
    if users[user_chat_id]:
        users[user_chat_id].locale = locale


def change_user_timezone_by_(user_chat_id: int, timezone: str) -> None:
    """Changes user timezone by the given user chat id and timezone."""
    with MySession() as session:
        session.execute(
            update(User)
            .where(User.chat_id == user_chat_id)
            .values(timezone=timezone)
        )
        session.commit()
    users[user_chat_id].timezone = timezone

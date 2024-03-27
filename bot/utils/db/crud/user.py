from typing import Union, List

from sqlalchemy import update
from sqlalchemy.orm import Session
from aiogram.types import User as TelegramUser

from ..models import User
from ..db import LocalSession, add_commit_and_refresh


def _get_user_by_(session: Session, user_chat_id: int) -> User:
    """Returns user by the given session and user chat id."""
    return session.query(User).filter(User.chat_id == user_chat_id).first()


def create_user_by_(telegram_user: TelegramUser) -> None:
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
    with LocalSession() as session:
        user = _get_user_by_(session, user_chat_id)
    return user


def get_user_locale_by_(user_chat_id: int) -> Union[str, None]:
    """Returns user language code by the given user chat id."""
    user = get_user_by_(user_chat_id)
    return user.locale if user else None


def get_all_users() -> List[User]:
    """Returns all users."""
    with LocalSession() as session:
        users = session.query(User).all()
    return users


def get_all_users_count() -> int:
    """Returns the count of all users."""
    with LocalSession() as session:
        count = session.query(User).count()
    return count


def get_all_mailing_users() -> List[User]:
    """Returns all mailing users."""
    with LocalSession() as session:
        users = session.query(User).filter(User.mailing).all()
    return users


def get_all_mailing_users_count() -> int:
    """Returns the count of all mailing users."""
    with LocalSession() as session:
        count = session.query(User).filter(User.mailing).count()
    return count


def change_user_locale_by_(user_chat_id: int, locale: str) -> None:
    """Changes user language by the given user chat id and language code."""
    with LocalSession() as session:
        session.execute(
            update(User)
            .where(User.chat_id == user_chat_id)
            .values(locale=locale)
        )
        session.commit()


def change_user_timezone_by_(user_chat_id: int, timezone: str) -> None:
    """Changes user timezone by the given user chat id and timezone."""
    with LocalSession() as session:
        session.execute(
            update(User)
            .where(User.chat_id == user_chat_id)
            .values(timezone=timezone)
        )
        session.commit()


def delete_user_with_(user_chat_id: int) -> None:
    """Deletes user with the given user chat id."""
    with LocalSession() as session:
        user = _get_user_by_(session, user_chat_id)
        session.delete(user)
        session.commit()

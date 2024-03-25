from typing import Union

from sqlalchemy import update
from sqlalchemy.orm import Session

from ..models import Mailing
from ..db import MySession, commit_and_refresh, add_commit_and_refresh


def _get_mailing_by_(session: Session, user_chat_id: int) -> Mailing:
    """Returns mailing by the given session and user chat id."""
    return (
        session.query(Mailing)
        .filter(Mailing.id_user_id == user_chat_id)
        .first()
    )


def get_mailing_by_(user_chat_id: int) -> Mailing:
    """Returns mailing by the given user chat id."""
    with MySession() as session:
        mailing = _get_mailing_by_(session, user_chat_id)
    return mailing

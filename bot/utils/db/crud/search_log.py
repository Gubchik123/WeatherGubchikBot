from typing import List

from sqlalchemy.orm import Session

from ..models import SearchLog
from ..db import LocalSession, commit_and_refresh


def _get_search_log_by_(
    session: Session, user_chat_id: int, city: str, locale: str
) -> SearchLog:
    """Returns user by the given session, user chat id and city."""
    return (
        session.query(SearchLog)
        .filter(
            SearchLog.user_id == user_chat_id,
            SearchLog.city == city,
            SearchLog.locale == locale,
        )
        .first()
    )


async def create_search_log(user_chat_id: int, city: str, locale: str) -> None:
    """Creates search log in database by the given user chat id and city."""
    city = city.split("(")[0].strip()

    with LocalSession() as session:
        search_log = _get_search_log_by_(session, user_chat_id, city, locale)
        if search_log is None:
            search_log = SearchLog(
                user_id=user_chat_id, city=city, locale=locale
            )
            session.add(search_log)
        else:
            search_log.count += 1
        return commit_and_refresh(session, search_log)


def get_last_4_search_cities_by_(user_chat_id: int, locale: str) -> List[str]:
    """Returns last 4 search log cities by the given user chat id and locale."""
    with LocalSession() as session:
        search_logs = (
            session.query(SearchLog)
            .filter(
                SearchLog.user_id == user_chat_id, SearchLog.locale == locale
            )
            .order_by(SearchLog.count.desc())
            .limit(4)
            .all()
        )
    return [search_log.city for search_log in search_logs]


def get_last_search_cities_by_(user_chat_id: int, locale: str) -> List[str]:
    """Returns last search log cities by the given user chat id and locale."""
    with LocalSession() as session:
        search_logs = (
            session.query(SearchLog)
            .filter(
                SearchLog.user_id == user_chat_id, SearchLog.locale == locale
            )
            .order_by(SearchLog.count.desc())
            .all()
        )
    return [search_log.city for search_log in search_logs]


def get_all_user_search_logs(user_chat_id: int) -> List[SearchLog]:
    """Returns all user search logs by the given user chat id."""
    with LocalSession() as session:
        search_logs = (
            session.query(SearchLog)
            .filter(SearchLog.user_id == user_chat_id)
            .order_by(SearchLog.count.desc())
            .all()
        )
    return search_logs


def delete_search_cities(
    user_chat_id: int, cities: List[str], locale: str
) -> None:
    """Deletes search log cities by the given user chat id and cities."""
    with LocalSession() as session:
        query = SearchLog.__table__.delete().where(
            SearchLog.user_id == user_chat_id,
            SearchLog.locale == locale,
            SearchLog.city.in_(cities),
        )
        session.execute(query)
        session.commit()

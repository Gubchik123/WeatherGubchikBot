from datetime import datetime
from pytz import timezone as tz

from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from .db import Base
from data.config import DEFAULT_LOCALE, DEFAULT_TIMEZONE


class User(Base):
    """Model for storing information about Telegram users."""

    __tablename__ = "users"
    # Fields from telegram user
    chat_id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(32), nullable=True, unique=True)
    full_name = Column(String(110), nullable=True, unique=False)
    # Settings fields
    locale = Column(String(2), nullable=False, default=DEFAULT_LOCALE)
    timezone = Column(String(32), nullable=False, default=DEFAULT_TIMEZONE)
    created = Column(DateTime, default=datetime.now(tz(DEFAULT_TIMEZONE)))
    # One-to-many relationship with SearchLog
    search_logs = relationship(
        "SearchLog",
        backref=backref("user", lazy="joined"),
        lazy="dynamic",
        passive_deletes=True,
    )
    # One-to-one relationship with Mailing
    mailing = relationship("Mailing", uselist=False, backref="user")


class SearchLog(Base):
    """Model for storing search logs."""

    __tablename__ = "search_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(64), nullable=False)
    locale = Column(String(2), nullable=False)
    count = Column(Integer, nullable=False, default=1)
    # One-to-many relationship with User
    user_id = Column(BigInteger, ForeignKey("users.chat_id"), nullable=False)


class Mailing(Base):
    """Model for storing mailing information."""

    __tablename__ = "mailing"

    id_user_id = Column(
        BigInteger,
        ForeignKey("users.chat_id"),
        primary_key=True,
        autoincrement=True,
    )
    mute = Column(Boolean, nullable=False, default=False)
    city = Column(String(64), nullable=False)
    time_int = Column(Integer, nullable=False)
    time_title = Column(String(32), nullable=False)
    # One-to-one relationship with WeatherProvider
    weather_provider_info = relationship(
        "WeatherProviderInfo", uselist=False, backref="mailing"
    )


class WeatherProviderInfo(Base):
    """Model for storing weather provider information."""

    __tablename__ = "weather_provider_info"

    id_mailing_id = Column(
        BigInteger,
        ForeignKey("mailing.id_user_id"),
        primary_key=True,
        autoincrement=True,
    )
    type = Column(String(32), nullable=False, default="weather")
    city = Column(String(64), nullable=False)
    time = Column(String(32), nullable=False)

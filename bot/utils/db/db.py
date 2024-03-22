from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from data.config import SQLALCHEMY_DATABASE_URL


# TODO: Async


engine = create_engine(SQLALCHEMY_DATABASE_URL)
MySession = sessionmaker(engine)

Base = declarative_base()


def commit_and_refresh(session: Session, model):
    """Commits and refreshes model instance and returns it."""
    session.commit()
    session.refresh(model)
    return model


def add_commit_and_refresh(model):
    """Adds, commits and refreshes model instance and returns it."""
    with MySession() as session:
        session.add(model)
        return commit_and_refresh(session, model)

import os

from sqlalchemy import create_engine as _create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv('DB_URL')


def create_engine(db_url=DB_URL,
                  echo=False):
    return _create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        echo=echo
    )


def create_session(engine):
    return sessionmaker(autocommit=False,
                        autoflush=False,
                        bind=engine)()

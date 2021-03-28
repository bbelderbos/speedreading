from sqlalchemy import create_engine as _create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgres://postgres:password@0.0.0.0:5435/speedreading"


def create_engine(db_url=SQLALCHEMY_DATABASE_URL,
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

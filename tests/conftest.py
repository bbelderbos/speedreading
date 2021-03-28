from datetime import datetime
import os

import pytest

from speedreading.database import (create_engine,
                                   create_session)
from speedreading.models import Base, User, Reading

TEST_DB_URL = os.getenv('TEST_DB_URL')


@pytest.fixture(scope="module")
def engine():
    engine = create_engine(TEST_DB_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def session(engine):
    session = create_session(engine)
    yield session
    session.rollback()


@pytest.fixture
def readings(session):
    readings = [
        Reading(end_time=datetime.now(),
                words_read=words)
        for words in (225, 297, 339)
    ]
    return readings


@pytest.fixture
def user(session, readings):
    user = User(email="tim@gmail.com",
                hashed_password="abc")
    user.readings = readings
    session.add(user)
    session.commit()
    return user

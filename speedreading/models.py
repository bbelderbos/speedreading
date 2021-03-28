from datetime import datetime

from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    readings = relationship("Reading",
                            back_populates="user")


class Text(Base):
    """Store some book texts for user for speed reading"""
    __tablename__ = "texts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    author = Column(String(50))
    text = Column(String)
    readings = relationship("Reading",
                            back_populates="text")


class Reading(Base):
    """Measure words user can read in a time span"""
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(
        DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    words_read = Column(Integer)
    text_id = Column(Integer, ForeignKey("texts.id"))
    text = relationship("Text", back_populates="readings")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="readings")


# this is cool:
# https://github.com/tiangolo/pydantic-sqlalchemy

PydanticUser = sqlalchemy_to_pydantic(User)
PydanticText = sqlalchemy_to_pydantic(Text)
PydanticReading = sqlalchemy_to_pydantic(Reading)


class PydanticUserWithReadings(PydanticUser):
    readings: list[PydanticReading] = []

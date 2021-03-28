from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .models import User, Text, Reading

# this is cool:
# https://github.com/tiangolo/pydantic-sqlalchemy

PydanticUser = sqlalchemy_to_pydantic(User)
PydanticText = sqlalchemy_to_pydantic(Text)
PydanticReading = sqlalchemy_to_pydantic(Reading)


class PydanticUserWithReadings(PydanticUser):
    readings: list[PydanticReading] = []

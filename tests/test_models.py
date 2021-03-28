from pydantic.error_wrappers import ValidationError
import pytest

from speedreading.models import User, Reading
from speedreading.schemas import (PydanticUser,
                                  PydanticUserWithReadings)


def test_orm_and_pydantic_models(session, user):
    assert session.query(User).count() == 1
    assert session.query(Reading).count() == 3
    first_user = session.query(User).first()
    assert first_user.email == 'tim@gmail.com'
    pydantic_user = PydanticUser.from_orm(user)
    data = pydantic_user.dict()
    assert data == {
        'id': 1,
        'email': 'tim@gmail.com',
        'hashed_password': 'abc',
        'is_active': True}
    pydantic_user_with_reading = (
        PydanticUserWithReadings.from_orm(user))
    data = pydantic_user_with_reading.dict()
    # nested pydantic model got created
    assert data['email'] == 'tim@gmail.com'
    assert len(data['readings']) == 3
    first, _, last = data['readings']
    assert first["words_read"] == 225
    assert last["words_read"] == 339


@pytest.mark.parametrize("kwargs, exception_error", [
    (dict(email=1),
     ('1 validation error for User\nid\n  '
      'field required (type=value_error.missing)')),
    (dict(id=2, email=(1, 2)),
     ('1 validation error for User\nemail\n  '
      'str type expected (type=type_error.str)')),
    (dict(id=2, email='bob@gmail.com', is_active='s'),
     ('1 validation error for User\nis_active\n  '
      'value could not be parsed to a boolean '
      '(type=type_error.bool)')),
])
def test_pydantic_model_validation(kwargs, exception_error):
    """It really is a Pydantic model I got for free!"""
    with pytest.raises(ValidationError) as exc:
        PydanticUser(**kwargs)
    assert str(exc.value) == exception_error

from speedreading.models import (User,
                                 PydanticUser,
                                 Reading,
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

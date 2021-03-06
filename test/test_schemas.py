import datetime
import pytest

from api.schema.user import (
    UserEntrySchema, UserResponseSchema, ValidationError)

@pytest.fixture(scope='function')
def user():
    return {"username": "jordan", "email": "mj@nba.com", "contactid": "23"}

def test_make_user_partial_schema(user):
    user1 = UserEntrySchema().load(user)
    assert user['username'] == user1['username']
    assert (set(user) | {'id', 'last_login', 'date_joined'}) == set(user1)

def test_make_user_dt_schema(user):
    for dt in [datetime.datetime.utcnow(), str(datetime.datetime.utcnow())]:
        user.update(date_joined=dt)
        user1 = UserEntrySchema().load(user)
        assert user1['date_joined'] < datetime.datetime.utcnow()
        assert user1['last_login'] > user1['date_joined']

def test_user_response_schema(user):
    user1 = UserResponseSchema().dump(UserResponseSchema().load(user))
    assert user['email'] == user1['email']
    assert {'email', 'roles', 'username'} == set(user1)
    assert [] == user1['roles']

def test_bad_user_schema(user):
    _ = user.pop('username')
    with pytest.raises(ValidationError, match='Missing data for required field'):
        user1 = UserEntrySchema().load(user)

def test_bad_user_email(user):
    user['email'] = ' i am funny '
    with pytest.raises(ValidationError, match='Not a valid email address'):
        user1 = UserEntrySchema().load(user)

def test_bad_user_resp_schema(user):
    _ = user.pop('username')
    with pytest.raises(ValidationError, match='Missing data for required field'):
        user1 = UserResponseSchema().load(user)

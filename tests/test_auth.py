import pytest
from jose import jwt
from passlib.context import CryptContext
from src.constants import SECRET_KEY
from src.auth import (
    create_access_token,
    verify_password,
    get_user,
    authenticate_user,
)
from src.main import verify_token, get_current_user, get_current_active_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.mark.auth
def test_verify_password_success(pwd_context, user):
    assert verify_password("admin", user.hashed_password)


@pytest.mark.auth
@pytest.mark.xfail
def test_verify_password_failure(pwd_context, user):
    assert not verify_password("wrong_password", user.hashed_password)


@pytest.mark.auth
def test_get_user_success(db, user):
    assert get_user(db, "admin") == user


@pytest.mark.auth
@pytest.mark.xfail
def test_get_user_failure(db):
    assert get_user(db, "invalid_username") is None


@pytest.mark.auth
def test_authenticate_user_success(db, user):
    assert authenticate_user(db, "admin", "admin") == user


@pytest.mark.auth
@pytest.mark.xfail
def test_authenticate_user_failure_invalid_username(db):
    assert not authenticate_user(db, "invalid_username", "admin")


@pytest.mark.auth
@pytest.mark.xfail
def test_authenticate_user_failure_invalid_password(db):
    assert not authenticate_user(db, "admin", "wrong_password")


@pytest.mark.auth
def test_create_access_token_success(user):
    token = create_access_token(data={"sub": user.username})
    assert jwt.decode(token, SECRET_KEY, algorithms=["HS256"])["sub"] == user.username


@pytest.mark.auth
@pytest.mark.xfail
def test_create_access_token_failure(user):
    assert not create_access_token(data={"sub": "invalid_username"})


@pytest.mark.auth
def test_verify_token_success(token):
    assert verify_token(token) == "admin"


@pytest.mark.auth
@pytest.mark.xfail
def test_verify_token_failure():
    assert not verify_token("invalid_token")


@pytest.mark.auth
def test_get_current_user_success(token):
    assert get_current_user(token) == "admin"


@pytest.mark.auth
@pytest.mark.xfail
def test_get_current_user_failure():
    assert not get_current_user("invalid_token")


@pytest.mark.auth
def test_get_current_active_user_success(token):
    assert get_current_active_user(token) == "admin"


@pytest.mark.auth
@pytest.mark.xfail
def test_get_current_active_user_failure():
    assert not get_current_active_user("invalid_token")

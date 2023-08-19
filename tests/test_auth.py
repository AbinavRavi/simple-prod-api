import pytest
from jose import jwt
from src.constants import SECRET_KEY
from src.auth import (
    create_access_token,
    verify_password,
)
from src.main import verify_token


@pytest.mark.auth
def test_verify_password_success(user):
    assert verify_password("admin", user.hashed_password)


@pytest.mark.auth
@pytest.mark.xfail
def test_verify_password_failure(user):
    assert not verify_password("wrong_password", user.hashed_password)


@pytest.mark.auth
def test_create_access_token_success(user):
    token = create_access_token(data={"sub": user.username})
    assert jwt.decode(token, SECRET_KEY, algorithms=["HS256"])["sub"] == user.username


@pytest.mark.auth
@pytest.mark.xfail
def test_create_access_token_failure(user):
    assert create_access_token(data={"sub": "invalid_username"})


@pytest.mark.auth
def test_verify_token_success(token):
    assert verify_token(token) == "admin"


@pytest.mark.auth
@pytest.mark.xfail
def test_verify_token_failure():
    assert verify_token("invalid_token") == "admin"

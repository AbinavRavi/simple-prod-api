import pytest
import sys
from os.path import abspath
from os.path import dirname as d
from passlib.context import CryptContext

parent_dir = f"{d(d(abspath(__file__)))}"
sys.path.append(f"{parent_dir}")
from src.main import app  # noqa
from fastapi.testclient import TestClient  # noqa
from src.model import UserInDB  # noqa
from src.auth import create_access_token, get_password_hash  # noqa


@pytest.fixture
def client():
    client = TestClient(app)
    yield client


@pytest.fixture
def db():
    user_dict = {
        "username": "admin",
        "email": "admin@admin.com",
        "full_name": "admin",
        "disabled": False,
        "hashed_password": get_password_hash("admin"),
    }
    yield {
        "admin": UserInDB(**user_dict),
    }


@pytest.fixture
def user(db):
    yield db["admin"]


@pytest.fixture
def pwd_context():
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    yield pwd


@pytest.fixture
def token():
    yield create_access_token(data={"sub": "admin"})

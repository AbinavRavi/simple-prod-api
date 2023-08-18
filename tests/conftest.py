import pytest
import sys
from os.path import abspath
from os.path import dirname as d

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
    yield {
        "admin": UserInDB(username="admin", hashed_password=get_password_hash("admin")),
    }


@pytest.fixture
def user(db):
    yield db["admin"]


@pytest.fixture
def token():
    yield create_access_token(data={"sub": "admin"})

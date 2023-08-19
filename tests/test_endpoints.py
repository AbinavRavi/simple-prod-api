import pytest
from src.model import OutputModel


@pytest.fixture
def get_token(client):
    payload = {
        "grant_type": "",
        "username": "admin",
        "password": "admin",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    token_response = client.post("/token", data=payload, headers=headers)
    token_res = token_response.json()
    token = token_res["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    yield header


@pytest.mark.endpoint
def test_health_check(client):
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.endpoint
def test_get_array(client, get_token):
    response = client.post("/get_array", json={"sentence": "Hello world"}, headers=get_token)
    res = OutputModel.model_validate(response.json())
    assert response.status_code == 200
    assert len(res.output) == 500


@pytest.mark.endpoint
@pytest.mark.xfail
def test_get_array_fail(client, get_token):
    response = client.post("/get_array", json={"sentence": None}, headers=get_token)
    assert response.status_code == 422
    assert response.json()["detail"] == {"sentence": ["This field is required."]}


@pytest.mark.endpoint
def test_get_array_different_data(client, get_token):
    for sentence in ["hello", "world"]:
        response = client.post("/get_array", json={"sentence": sentence}, headers=get_token)
        assert response.status_code == 200
        assert len(response.json()["output"]) == 500

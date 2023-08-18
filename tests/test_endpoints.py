import pytest
from src.model import OutputModel


@pytest.mark.endpoint
def test_health_check(client):
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.endpoint
def test_get_array(client):
    response = client.post("/get_array", json={"sentence": "Hello world"})
    res = OutputModel.model_validate(response.json())
    assert response.status_code == 200
    assert len(res.output) == 500


@pytest.mark.endpoint
@pytest.mark.xfail
def test_get_array_fail(client):
    response = client.post("/get_array", json={"sentence": ""})
    assert response.status_code == 422
    assert response.json()["detail"] == {"sentence": ["This field is required."]}


@pytest.mark.endpoint
def test_get_array_different_data(client):
    for sentence in ["hello", "world"]:
        response = client.post("/get_array", json={"sentence": sentence})

        assert response.status_code == 200
        assert len(response.json()["output"]) == 500

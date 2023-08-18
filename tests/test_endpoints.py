import pytest
from model import OutputModel


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
    pass

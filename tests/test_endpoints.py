import pytest
from model import OutputModel
from typing import List


@pytest.mark.endpoint
def test_health_check(client):
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.endpoint
def test_get_array(client):
    response = client.post("/get_array")
    res = OutputModel.model_validate(response.json())
    assert response.status_code == 200
    assert isinstance(res.output, List[float])
    assert len(res.output) == 500

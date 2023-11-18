import pytest


def test_innerdia(_client):
    response = _client.get("/api/innerdia?nps=2.500&sch=40")
    assert response.status_code == 200
    assert response.json.get("innerdia") == "2.469"

    response = _client.get("/api/innerdia?nps=not-a-nps&sch=40")
    assert response.status_code == 401
    assert response.json.get("message") == "Invalid 'nps' or 'sch'"

def test_time(_client):
    response = _client.get("/api/time")
    assert response.status_code == 200


def test_protected_time(_client):
    response = _client.get("/api/protected/time")
    assert response.status_code == 401

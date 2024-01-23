import pytest


def test_transactions(_client):
    response = _client.get("/api/transactions")
    assert response.status_code == 200
    # FIXME: Assert response for GET /transactions
    # assert response.json == []


def test_transaction(_client):
    response = _client.get("/api/transactions/1")
    assert response.status_code == 200
    # FIXME: Assert response for GET /transactions/1
    # assert response.json == {}

    response = _client.get("/api/transactions/0")
    assert response.status_code == 401
    # FIXME: Assert response for bad GET /transactions
    # assert response.json.get("message") == "Invalid 'id'"

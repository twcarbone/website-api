import pytest


def test_innerdia(_client):
    response = _client.get("/api/innerdia?nps=2.500&sch=40")
    assert response.status_code == 200
    assert response.json.get("innerdia") == "2.469"

    response = _client.get("/api/innerdia?nps=not-a-nps&sch=40")
    assert response.status_code == 401
    assert response.json.get("message") == "Invalid 'nps' or 'sch'"

    # TODO: Pending resolution of #8, test for missing query parameters


def test_pipesize(_client):
    response = _client.get("/api/pipesize/10")
    assert response.status_code == 200
    assert response.json == {"id": 10, "nps": "2.500", "outer_dia": 2.875, "outer_dia_unit_id": 1}

    response = _client.get("/api/pipesize/999")
    assert response.status_code == 401
    assert response.json.get("message") == "Invalid 'id'"


def test_pipesizes(_client):
    response = _client.get("/api/pipesizes")
    assert response.status_code == 200
    assert response.json == [
        {"id": 1, "nps": "0.125", "outer_dia_unit_id": 1, "outer_dia": 0.405},
        {"id": 2, "nps": "0.250", "outer_dia_unit_id": 1, "outer_dia": 0.54},
        {"id": 3, "nps": "0.375", "outer_dia_unit_id": 1, "outer_dia": 0.675},
        {"id": 4, "nps": "0.500", "outer_dia_unit_id": 1, "outer_dia": 0.84},
        {"id": 5, "nps": "0.750", "outer_dia_unit_id": 1, "outer_dia": 1.05},
        {"id": 6, "nps": "1.000", "outer_dia_unit_id": 1, "outer_dia": 1.315},
        {"id": 7, "nps": "1.250", "outer_dia_unit_id": 1, "outer_dia": 1.66},
        {"id": 8, "nps": "1.500", "outer_dia_unit_id": 1, "outer_dia": 1.9},
        {"id": 9, "nps": "2.000", "outer_dia_unit_id": 1, "outer_dia": 2.375},
        {"id": 10, "nps": "2.500", "outer_dia_unit_id": 1, "outer_dia": 2.875},
        {"id": 11, "nps": "3.000", "outer_dia_unit_id": 1, "outer_dia": 3.5},
        {"id": 12, "nps": "3.500", "outer_dia_unit_id": 1, "outer_dia": 4.0},
        {"id": 13, "nps": "4.000", "outer_dia_unit_id": 1, "outer_dia": 4.5},
        {"id": 14, "nps": "5.000", "outer_dia_unit_id": 1, "outer_dia": 5.563},
        {"id": 15, "nps": "6.000", "outer_dia_unit_id": 1, "outer_dia": 6.625},
        {"id": 16, "nps": "8.000", "outer_dia_unit_id": 1, "outer_dia": 8.625},
        {"id": 17, "nps": "10.000", "outer_dia_unit_id": 1, "outer_dia": 10.75},
        {"id": 18, "nps": "12.000", "outer_dia_unit_id": 1, "outer_dia": 12.75},
        {"id": 19, "nps": "14.000", "outer_dia_unit_id": 1, "outer_dia": 14.0},
        {"id": 20, "nps": "16.000", "outer_dia_unit_id": 1, "outer_dia": 16.0},
        {"id": 21, "nps": "18.000", "outer_dia_unit_id": 1, "outer_dia": 18.0},
        {"id": 22, "nps": "20.000", "outer_dia_unit_id": 1, "outer_dia": 20.0},
        {"id": 23, "nps": "22.000", "outer_dia_unit_id": 1, "outer_dia": 22.0},
        {"id": 24, "nps": "24.000", "outer_dia_unit_id": 1, "outer_dia": 24.0},
        {"id": 25, "nps": "30.000", "outer_dia_unit_id": 1, "outer_dia": 30.0},
        {"id": 26, "nps": "32.000", "outer_dia_unit_id": 1, "outer_dia": 32.0},
        {"id": 27, "nps": "34.000", "outer_dia_unit_id": 1, "outer_dia": 34.0},
        {"id": 28, "nps": "36.000", "outer_dia_unit_id": 1, "outer_dia": 36.0},
        {"id": 29, "nps": "42.000", "outer_dia_unit_id": 1, "outer_dia": 42.0},
    ]

from api import db
from api import models


def test_register(_init_db, _client, _new_user_dict):
    response = _client.post("/api/register", json=_new_user_dict)
    assert response.status_code == 200

    user = db.session.get(models.User, 2)
    assert user.id == 2
    assert user.email == "cheese@gmail.com"
    assert type(user.pwhash) == bytes
    assert len(user.pwhash) == 60

    assert db.session.get(models.User, 3) is None


def test_register_missing_params(_init_db, _client):
    response = _client.post("/api/register", json={"email": "foo"})
    assert response.status_code == 200
    assert response.data == b"Missing password\n"

    response = _client.post("/api/register", json={"email": "foo", "password": ""})
    assert response.status_code == 200
    assert response.data == b"Missing password\n"


def test_login(_init_db, _client, _existing_user_dict):
    response = _client.post("api/login", json=_existing_user_dict)
    assert response.status_code == 200
    # TODO: Test for valid JWT in test_login
    assert type(response.get_json().get("access_token")) == str


def test_login_invalid_password(_init_db, _client, _existing_user_dict):
    response = _client.post("api/login", json={"email": "bean@gmail.com", "password": "wrong-password"})
    assert response.status_code == 200
    assert response.data == b"Wrong email or password\n"

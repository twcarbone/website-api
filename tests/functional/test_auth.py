import uuid

import flask_jwt_extended

from api import db
from api.models.auth import User

# ------------
# Test helpers
# ------------


def _test_jwt(encoded_token: str):
    decoded_token = flask_jwt_extended.decode_token(encoded_token=encoded_token)

    assert list(decoded_token.keys()) == ["fresh", "iat", "jti", "type", "sub", "nbf", "exp"]

    assert decoded_token.get("fresh") == False
    assert decoded_token.get("sub") == 1
    assert decoded_token.get("type") == "access"

    # Test for valid UUID
    uuid_str = decoded_token.get("jti")
    assert str(uuid.UUID(uuid_str)) == uuid_str


# -----
# Tests
# -----


def test_register(_init_db, _client, _new_user_dict):
    response = _client.post("/api/register", json=_new_user_dict)
    assert response.status_code == 200

    user = db.session.get(User, 2)
    assert user.id == 2
    assert user.email == "cheese@gmail.com"
    assert type(user.pwhash) == bytes
    assert len(user.pwhash) == 60

    assert db.session.get(User, 3) is None


def test_register_missing_params(_init_db, _client):
    response = _client.post("/api/register", json={"email": "foo"})
    assert response.status_code == 422
    assert response.json.get("message") == "Missing password"

    response = _client.post("/api/register", json={"email": "foo", "password": ""})
    assert response.status_code == 422
    assert response.json.get("message") == "Missing password"


def test_login(_init_db, _client, _existing_user_dict):
    response = _client.post("api/login", json=_existing_user_dict)
    assert response.status_code == 200
    _test_jwt(response.json.get("access_token"))


def test_login_invalid_password(_init_db, _client, _existing_user_dict):
    response = _client.post("api/login", json={"email": "bean@gmail.com", "password": "wrong-password"})
    assert response.status_code == 401
    assert response.json.get("message") == "Wrong email or password"

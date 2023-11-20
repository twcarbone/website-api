import json

import pytest

import api
from api import db
from api.models.auth import User
from api.models.engdata import PipeSize

import config

# --------------------------
# Flask test client fixtures
# --------------------------


@pytest.fixture
def _app():
    return api.create_app(config_class=config.TestConfig)


@pytest.fixture
def _client(_app):
    with _app.test_client() as client:
        with _app.app_context() as ctx:
            yield client


@pytest.fixture
def _runner(_app):
    return _app.test_cli_runner()


# -----------------
# Database fixtures
# -----------------


@pytest.fixture
def _init_db(_client):
    """
    Initialize the test database to support testing.

    Drop and re-create tables, add mock data, etc.
    """
    # Only drop/create the necessary tables
    User.__table__.drop(db.engine)
    User.__table__.create(db.engine)

    db.session.add(User(email="bean@gmail.com", password="catnip"))
    db.session.commit()


# -------------
# User fixtures
# -------------


@pytest.fixture
def _existing_user_dict():
    return {"email": "bean@gmail.com", "password": "catnip"}


@pytest.fixture
def _existing_user_jwt(_client, _existing_user_dict):
    return _client.post("api/login", json=_existing_user_dict).get_json().get("access_token")


@pytest.fixture
def _existing_user_header_bearer(_existing_user_jwt):
    return {"Authorization": f"Bearer {_existing_user_jwt}"}


@pytest.fixture
def _new_user_dict():
    return {"email": "cheese@gmail.com", "password": "my-favorite-bone"}


@pytest.fixture
def _new_user_json(_new_user_dict):
    return json.dumps(_new_user_dict)


@pytest.fixture
def _new_user(_new_user_dict):
    return User(**_new_user_dict)


# -----------------
# PipeSize fixtures
# -----------------


@pytest.fixture
def _pipesize(_client):
    return db.session.get(PipeSize, 10)

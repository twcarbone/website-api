import json

import pytest

import api
from api import db
from api import models

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
    db.drop_all()
    db.create_all()

    db.session.add(models.User(email="bean@gmail.com", password="catnip"))
    db.session.commit()


# -------------
# User fixtures
# -------------


@pytest.fixture
def _existing_user_dict():
    return {"email": "bean@gmail.com", "password": "catnip"}


@pytest.fixture
def _new_user_dict():
    return {"email": "cheese@gmail.com", "password": "my-favorite-bone"}


@pytest.fixture
def _new_user_json(_new_user_dict):
    return json.dumps(_new_user_dict)


@pytest.fixture
def _new_user(_new_user_dict):
    return models.User(**_new_user_dict)

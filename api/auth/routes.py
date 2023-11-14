import logging

import flask
import flask_jwt_extended

import api.models as models
import api.utils as utils
from api import db
from api import jwt
from api.auth import bp


@jwt.user_identity_loader
def user_identity_lookup(user: models.User) -> int:
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    id = jwt_data["sub"]
    return db.session.get(models.User, id)


@bp.route("/register", methods=["POST"])
@utils.requires_request_params(["email", "password"])
def register():
    email = flask.request.json.get("email")
    password = flask.request.json.get("password")

    user = models.User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    logging.info(f"Successfully added new {user}")

    return f"Welcome, '{email}'\n"


@bp.route("/login", methods=["POST"])
@utils.requires_request_params(["email", "password"])
def login():
    email = flask.request.json.get("email")
    password = flask.request.json.get("password")

    user = db.session.execute(db.select(models.User).filter_by(email=email)).scalar()

    if user is None or not user.checkpw(password):
        return "Wrong email or password\n"

    return flask.jsonify(access_token=flask_jwt_extended.create_access_token(identity=user))
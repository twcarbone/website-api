import logging

import flask
import flask_jwt_extended

import api.utils as utils
from api import db
from api import jwt
from api.auth import bp
from api.errors.handlers import APIError
from api.models.auth import User


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> int:
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    id = jwt_data["sub"]
    return db.session.get(User, id)


@bp.route("/register", methods=["POST"])
@utils.requires_request_params(["email", "password"])
def register():
    email = flask.request.json.get("email")
    password = flask.request.json.get("password")

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    logging.info(f"Successfully added new {user}")

    return f"Welcome, '{email}'\n"


@bp.route("/login", methods=["POST"])
@utils.requires_request_params(["email", "password"])
def login():
    email = flask.request.json.get("email")
    password = flask.request.json.get("password")

    user = db.session.execute(db.select(User).filter_by(email=email)).scalar()

    if user is None or not user.checkpw(password):
        raise APIError("Wrong email or password", status_code=401)

    return flask.jsonify(access_token=flask_jwt_extended.create_access_token(identity=user))

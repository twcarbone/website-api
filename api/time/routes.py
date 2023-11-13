import logging
import time

import flask_jwt_extended

import api.utils as utils
from api import jwt
from api.time import bp


@bp.route("/time", methods=["GET"])
def get_time():
    return {"time": time.time()}


@bp.route("/protected/time", methods=["GET"])
@flask_jwt_extended.jwt_required()
def get_protected_time():
    return {"time": time.time()}

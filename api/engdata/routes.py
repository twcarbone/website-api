import flask

from api.engdata import bp
from api.errors.handlers import APIError
from api.models import exc
from api.models.engdata import PipeSize


# TODO: (#8) Create utility for missing GET query parameters
@bp.route("/innerdia", methods=["GET"])
def innerdia():
    nps = flask.request.args.get("nps")
    sch = flask.request.args.get("sch")

    try:
        return flask.jsonify(innerdia=PipeSize.inner_dia(nps, sch))
    except ValueError as err:
        raise APIError("Invalid 'nps' or 'sch'", status_code=401) from err


# --------
# PipeSize
# --------


@bp.route("/pipesizes", methods=["GET"])
def pipesizes():
    return flask.jsonify(PipeSize.serialize_sequence(PipeSize.scalars()))


@bp.route("pipesize/<int:id>", methods=["GET"])
def pipesize(id):
    try:
        return flask.jsonify(PipeSize.scalar_one(id=id).serialize())
    except exc.NoResultFound as err:
        raise APIError("Invalid 'id'", status_code=401) from err

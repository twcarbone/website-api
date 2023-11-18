import flask

from api.engdata import bp
from api.errors.handlers import APIError
from api.models.engdata import PipeSize


@bp.route("/innerdia", methods=["GET"])
def innerdia():
    nps = flask.request.args.get("nps")
    sch = flask.request.args.get("sch")

    try:
        return flask.jsonify(innerdia=PipeSize.inner_dia(nps, sch))
    except ValueError as err:
        raise APIError("Invalid 'nps' or 'sch'", status_code=401) from err

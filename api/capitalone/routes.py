from typing import Type

import flask
from flask import request

import api.models.capitalone as models
from api.capitalone import bp
from api.errors.handlers import APIError
from api.models import exc


def get_many(model: Type[models._CapitalOneBase], **kwargs):
    return flask.jsonify(model.serialize_sequence(model.scalars(**request.args)))


def get_one(model: Type[models._CapitalOneBase], id):
    try:
        return flask.jsonify(model.scalar_one(id=id).serialize())
    except exc.NoResultFound as err:
        raise APIError("Invalid 'id'", status_code=401) from err


@bp.route("/cards", methods=["GET"])
def cards():
    return get_many(models.Card, **request.args)


@bp.route("/cards/<int:id>", methods=["GET"])
def card(id):
    return get_one(models.Card, id)


@bp.route("/transactions", methods=["GET"])
def transactions():
    return get_many(models.TransactionView, **request.args)


@bp.route("/transactions/<int:id>", methods=["GET"])
def transaction(id):
    return get_one(models.TransactionView, id)

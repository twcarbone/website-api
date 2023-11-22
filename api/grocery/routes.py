import flask

from api.errors.handlers import APIError
from api.grocery import bp
from api.models import exc
from api.models.grocery import OrderView
from api.models.grocery import ProductView
from api.models.grocery import TransactionView


@bp.route("/products", methods=["GET"])
def products():
    return flask.jsonify(ProductView.serialize_sequence(ProductView.scalars()))


@bp.route("/product/<int:id>", methods=["GET"])
def product(id):
    try:
        return flask.jsonify(ProductView.scalar_one(id=id).serialize())
    except exc.NoResultFound as err:
        raise APIError("Invalid 'id'", status_code=401) from err


@bp.route("/orders", methods=["GET"])
def orders():
    return flask.jsonify(OrderView.serialize_sequence(OrderView.scalars()))


@bp.route("/order/<int:id>", methods=["GET"])
def order(id):
    try:
        return flask.jsonify(OrderView.scalar_one(id=id).serialize())
    except exc.NoResultFound as err:
        raise APIError("Invalid 'id'", status_code=401) from err


@bp.route("/transactions", methods=["GET"])
def transactions():
    return flask.jsonify(TransactionView.serialize_sequence(TransactionView.scalars()))


@bp.route("/transaction/<int:id>", methods=["GET"])
def transaction(id):
    try:
        return flask.jsonify(TransactionView.scalar_one(id=id).serialize())
    except exc.NoResultFound as err:
        raise APIError("Invalid 'id'", status_code=401) from err

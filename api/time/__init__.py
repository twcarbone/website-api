from flask import Blueprint

bp = Blueprint("time", __name__)

from api.time import routes

from flask import Blueprint

bp = Blueprint("engdata", __name__)

from api.engdata import routes

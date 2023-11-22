from flask import Blueprint

bp = Blueprint("grocery", __name__)

from api.grocery import routes

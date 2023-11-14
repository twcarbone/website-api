from flask import Blueprint

bp = Blueprint("errors", __name__)

from api.errors import handlers

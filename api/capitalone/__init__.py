from flask import Blueprint

bp = Blueprint("capitalone", __name__)

from api.capitalone import routes

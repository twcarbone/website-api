import flask

from api.errors import bp


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@bp.app_errorhandler(APIError)
def api_error(e):
    return flask.jsonify(e.to_dict()), e.status_code

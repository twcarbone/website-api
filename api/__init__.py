import logging

import flask
import flask_jwt_extended
import flask_sqlalchemy

import api.log
import api.models

import config

jwt = flask_jwt_extended.JWTManager()
db = flask_sqlalchemy.SQLAlchemy(model_class=api.models.Base)


def create_app(config_class=config.ProdConfig):
    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    jwt.init_app(app)
    db.init_app(app)

    from api.errors import bp as errors_bp

    app.register_blueprint(errors_bp, url_prefix="/api")

    from api.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api")

    from api.time import bp as time_bp

    app.register_blueprint(time_bp, url_prefix="/api")

    return app

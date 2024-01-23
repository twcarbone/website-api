import logging

import flask
import flask_jwt_extended
import flask_sqlalchemy
import pint

import api.log
import api.models

import config

jwt = flask_jwt_extended.JWTManager()
db = flask_sqlalchemy.SQLAlchemy(model_class=api.models.Base)
ureg = pint.UnitRegistry()


def create_app(config_class=config.ProdConfig):
    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    jwt.init_app(app)
    db.init_app(app)

    from api.errors import bp as errors_bp

    app.register_blueprint(errors_bp, url_prefix="/api")

    from api.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api")

    from api.engdata import bp as engdata_bp

    app.register_blueprint(engdata_bp, url_prefix="/api")

    from api.grocery import bp as grocery_bp

    app.register_blueprint(grocery_bp, url_prefix="/api")

    from api.capitalone import bp as capitalone_bp

    app.register_blueprint(capitalone_bp, url_prefix="/api")

    from api.time import bp as time_bp

    app.register_blueprint(time_bp, url_prefix="/api")

    return app


import api.models.auth
import api.models.capitalone
import api.models.engdata
import api.models.grocery

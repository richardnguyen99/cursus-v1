# -*- coding: utf-8 -*-

"""Cursus app factory module
"""

import os
import flask

from flask import Flask

from .views import find_bp
from .util.extensions import db, migrate


def create_app() -> Flask:
    """App factory function to create a Flask app instance

    The pattern is carefully described in the Flask documentation

    :see https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
    """

    # Create a Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration for the application
    app.config.from_object(os.environ.get("APP_SETTINGS"))

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/ping")
    def ping():
        resp = flask.make_response(flask.json.dumps({"message": "pong"}), 200)
        resp.headers["Content-Type"] = "application/json"

        return resp

    @app.route("/")
    def hello():
        resp = flask.make_response(
            flask.json.dumps({"message": "Welcome to the Cursus API"}), 200
        )
        resp.headers["Content-Type"] = "application/json"

        return resp

    @app.route("/config")
    def config():
        return flask.jsonify({"message": app.config["DATABASE_URL"]})

    app.register_blueprint(find_bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):  # pylint: disable=unused-argument
        db.session.remove()

    return app

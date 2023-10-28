# -*- coding: utf-8 -*-

"""OS module providing functionalities to work with operating system"""
import os

import flask
from flask import Flask


def create_app() -> Flask:
    """App factory function to create a Flask app instance

    The pattern is carefully described in the Flask documentation

    :see https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
    """

    # Create a Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration for the application
    app.config.from_object(os.environ.get("APP_SETTINGS"))

    @app.route("/")
    def hello():
        return flask.jsonify({"message": "Hello, World!"})

    @app.route("/config")
    def config():
        return flask.jsonify({"message": app.config["DATABASE_URL"]})

    return app

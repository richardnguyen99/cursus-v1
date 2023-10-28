import os

import flask
from flask import Flask


def create_app(test_config=None):
    # Create a Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration for the application

    @app.route("/")
    def hello():
        return flask.jsonify({"message": "Hello, World!"})

    return app

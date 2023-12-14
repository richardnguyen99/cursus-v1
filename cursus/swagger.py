# -*- coding: utf-8 -*-

"""Cursus Swagger (OpenAPI) module

This submodule contains configuration for Swagger (OpenAPI) documentation.
"""

import flask

from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = (
    "/api/v1/docs/"  # URL for exposing Swagger UI (without trailing '/')
)
API_URL = flask.current_app.config["SWAGGER_API_SPEC_URL"]


# Call factory function to create our blueprint
def swagger_blueprint():
    return get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Cursus application"},
    )

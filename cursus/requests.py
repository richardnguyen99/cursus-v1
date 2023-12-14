# -*- coding: utf-8 -*-

"""Cursus general requests module

This submodule contains request handlers for general purposes such as logging
and serving static files.

To see the request handlers for the blueprints, see the cursus/views/ for web
app and cursus/apis/ for REST API.
"""

import flask
import datetime


def _make_response_cache(req: flask.Request, response: flask.Response):
    # Cache static assets for 1 year
    response.add_etag()
    response.last_modified = datetime.datetime.utcnow()

    response.access_control_allow_methods = ["GET"]
    response.access_control_allow_origin = "*"
    response.access_control_max_age = 3600

    # If the client wishes to send a no-cache header, the content of
    # static files will not be cached
    if (
        "Cache-Control" in req.headers
        and req.headers["Cache-Control"] == "no-cache"
    ):
        return

    response.headers["Cache-Control"] = "public, max-age=31536000"


def after(response: flask.Response):
    current_app = flask.current_app
    req = flask.request

    current_app.logger.info(
        f'"{req.remote_addr}" {req.method} {req.path} \
{response.status_code} {response.content_length}'
    )

    if req.path.startswith("/static"):
        _make_response_cache(req, response)
        return response.make_conditional(req)

    return response

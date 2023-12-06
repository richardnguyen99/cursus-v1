"""View module for the Cursus App
"""

import flask
import datetime

from .oauth import authorize, callback

SUPPORT_PUBLIC_ENDPOINTS = {
    "",
    "about",
    "demo",
    "docs",
}

view_bp = flask.Blueprint(
    "views",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

oauth_bp = flask.Blueprint("oauth", __name__, url_prefix="/oauth")

oauth_bp.add_url_rule(
    "/authorize/<provider>",
    view_func=authorize,
    methods=["GET"],
)

oauth_bp.add_url_rule(
    "/callback/<provider>",
    view_func=callback,
    methods=["GET"],
)


@view_bp.after_request
def after(response: flask.Response):
    req = flask.request
    if "X-Response-SPA" in response.headers:
        return response

    response.add_etag()
    if (
        "Cache-Control" in response.headers
        and response.headers["Cache-Control"] == "no-cache"
    ):
        return response.make_conditional(req)

    response.headers["Cache-Control"] = "public, max-age=0, must-revalidate"

    return response.make_conditional(flask.request)


from . import public
from . import protected
from . import error

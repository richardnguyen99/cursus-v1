"""View module for the Cursus App
"""

import flask

from werkzeug.exceptions import BadRequest, NotFound

from cursus.util import exceptions

SUPPORT_ENDPOINTS = [
    "",
    "about",
]

view_bp = flask.Blueprint(
    "views",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)


@view_bp.app_errorhandler(exceptions.BadRequestError)
@view_bp.app_errorhandler(BadRequest)
@view_bp.app_errorhandler(400)
def handle_bad_request(error):
    req = flask.request
    msg = f"Bad Request: {req.method} {req.url}"

    if isinstance(error, BadRequest):
        msg = error.get_description()
    elif isinstance(error, exceptions.BadRequestError):
        msg = error.get_reason()

    return flask.render_template("400.html", msg=msg), 400


@view_bp.app_errorhandler(exceptions.NotFoundError)
@view_bp.app_errorhandler(NotFound)
@view_bp.app_errorhandler(404)
def handle_not_found(error):
    req = flask.request
    msg = f"Not found: {req.url}"

    if isinstance(error, NotFound):
        msg = error.get_description()
    elif isinstance(error, exceptions.NotFoundError):
        msg = error.get_reason()

    return (
        flask.render_template(
            "4xx.html",
            title="Not found",
            status_message="Not found",
            status_code=404,
            reason=msg,
        ),
        404,
    )


@view_bp.route("/", defaults={"page_name": "index"}, methods=["GET"])
@view_bp.route("/<page_name>", methods=["GET"])
def show(page_name):
    req = flask.request
    current_app = flask.current_app

    url = req.path
    endpoint = url.split("/")[1]

    if endpoint not in SUPPORT_ENDPOINTS:
        raise exceptions.NotFoundError(f"Page {page_name} not found")

    if req.method != "GET":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    resp = flask.render_template(f"{page_name}.html")

    current_app.logger.info(
        f'({req.remote_addr}) - "{req.method} {req.url}" 200 {len(resp)}'
    )

    return resp, 200

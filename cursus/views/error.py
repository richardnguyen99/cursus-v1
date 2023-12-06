# -*- coding: utf-8 -*-

"""Cursus error module for handling HTTP errors
"""

import flask

from werkzeug import exceptions as WkzExceptions

from . import view_bp
from ..util import exceptions as CursusExceptions


@view_bp.app_errorhandler(CursusExceptions.NotFoundError)
@view_bp.app_errorhandler(WkzExceptions.NotFound)
def handle_not_found(error) -> flask.Response:
    """Error handler for not founding a page

    By default, Flask will return a 404 response when it cannot find a page
    to serve the incoming request. This function overrides the default
    behavior and returns a custom 404 response.

    Other routes under the `view_bp` blueprint can raise the
    `CursusExceptions.NotFoundError` exception and this function will catch
    the error. For example::

        @view_bp.route("/<page_name>")
        def show(page_name: str):
            if page_name not in SUPPORT_PUBLIC_ENDPOINTS:
                raise CursusExceptions.NotFoundError(
                        f"Page {page_name} not found"
                )

            ...

    Args:
        error (`type[Exception]`): An integer value or an exception
        object that repsernts the 404 HTTP status code

    Returns:
        `tuple[str, int]`: A tuple containing the HTML response with the
        404 status code
    """

    req = flask.request
    msg = f"Not found: {req.url}"
    code = 400
    code_msg = "Bad Request"

    if isinstance(error, CursusExceptions.CursusError):
        msg = str(error)
        code = error.status_code
        code_msg = error.status_msg
    elif isinstance(error, WkzExceptions.HTTPException):
        msg = error.get_description()
        code = error.code or 400
        code_msg = error.name

    if "application/json" in req.headers["Accept"]:
        return flask.json.jsonify(
            {
                "error": {
                    "code": code,
                    "message": code_msg,
                    "reason": msg,
                }
            },
            code,
        )

    return flask.make_response(
        flask.render_template(
            "4xx.html",
            title=code_msg,
            status_message=code_msg,
            status_code=code,
            reason=msg,
        ),
        code,
    )

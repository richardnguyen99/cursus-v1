# -*- coding: utf-8 -*-

"""Cursus error module for handling HTTP errors
"""

import flask

from werkzeug import exceptions as WkzExceptions

from .util import exceptions as CursusExceptions


def handle_not_found(error) -> tuple[str, int]:
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
        error (`type[Exception] | int`): An integer value or an exception
        object that repsernts the 404 HTTP status code

    Returns:
        `tuple[str, int]`: A tuple containing the HTML response with the
        404 status code
    """

    req = flask.request
    msg = f"Not found: {req.url}"

    if isinstance(error, CursusExceptions.NotFoundError):
        msg = str(error)
    elif isinstance(error, WkzExceptions.NotFound):
        msg = error.get_description()

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

# -*- coding: utf-8 -*-

"""List of custom exceptions used by the Cursus application
"""

import flask
import flask_login
import flask_caching
import werkzeug.exceptions as WkzExceptions


from . import view_bp, docs
from cursus.util import exceptions as CursusExceptions
from cursus.util.extensions import db, cache

SUPPORT_PUBLIC_ENDPOINTS = {
    "",
    "about",
    "demo",
    "docs",
}


@view_bp.route("/login", methods=["GET", "HEAD"])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("views.show", page_name="index"))

    req = flask.request

    if req.method != "GET" and req.method != "HEAD":
        raise CursusExceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    # Redirect to the next page after logging in
    next = req.args.get("next")

    return flask.render_template("login.html", next=next), 200


@view_bp.route("/", defaults={"page_name": "index"})
@view_bp.route("/<page_name>")
def show(page_name: str):
    req = flask.request
    url = req.path
    endpoint = url.split("/")[1]

    if endpoint not in SUPPORT_PUBLIC_ENDPOINTS:
        raise CursusExceptions.NotFoundError(f"Page {page_name} not found")

    if req.method != "GET" and req.method != "HEAD":
        raise CursusExceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    resp = flask.render_template(
        f"{page_name}.html",
        page_name=page_name,
        current_user=flask_login.current_user,
    )

    return resp, 200


view_bp.register_blueprint(docs.view_doc_bp)

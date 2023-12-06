# -*- coding: utf-8 -*-

"""Sub view module for Cursus Application's documentation pages
"""

import flask

from cursus.util.exceptions import NotFoundError

SUPPRORT_DOC_ENDPOINTS = (
    "",
    "search",
    "details",
    "courses",
    "campus",
    "domains",
    "more",
)

view_doc_bp = flask.Blueprint(
    "docs",
    __name__,
    url_prefix="/docs",
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)


@view_doc_bp.route("/")
def show_main_doc():
    return flask.render_template("docs.html", page_name="docs")


@view_doc_bp.route("/<page_name>")
def show(page_name: str):
    if page_name not in SUPPRORT_DOC_ENDPOINTS:
        raise NotFoundError(f"Page {page_name} not found")

    resp = flask.render_template(
        f"doc-{page_name}.html",
        page_name=page_name,
    )

    return resp

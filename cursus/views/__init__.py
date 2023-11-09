"""View module for the Cursus App
"""

import flask
import jinja2

view_bp = flask.Blueprint(
    "views",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)


@view_bp.route("/", defaults={"page_name": "index"}, methods=["GET"])
@view_bp.route("/<page_name>", methods=["GET"])
def show(page_name):
    try:
        return flask.render_template(f"{page_name}.html")
    except jinja2.TemplatesNotFound:
        flask.abort(404)

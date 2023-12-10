# -*- coding: utf-8 -*-

"""Cursus general routes module

This submodule contains general routes that are not related to or handled by
any specific blueprint.

To see the routes handled by the blueprints, see the cursus/views/ for web app 
and  cursus/apis/ for REST API.
"""


import os
import flask
import flask_login


@flask.current_app.route("/logout")
@flask_login.login_required
def logout():
    flask.logout_user()
    return flask.redirect(flask.url_for("views.show", page_name="index"))


@flask.current_app.route("/ping")
def ping():
    resp = flask.make_response(flask.json.dumps({"message": "pong"}), 200)
    resp.headers["Content-Type"] = "application/json"

    return resp


@flask.current_app.route("/sw.js")
def sw():
    resp = flask.make_response(
        flask.send_from_directory("static", "sw.js"), 200
    )
    resp.headers["Content-Type"] = "application/javascript"
    resp.headers["Cache-Control"] = "no-cache"

    return resp


@flask.current_app.route("/robots.txt")
def robots():
    resp = flask.make_response(
        flask.send_from_directory("static", "robots.txt"), 200
    )
    resp.headers["Content-Type"] = "text/plain"
    resp.headers["Cache-Control"] = "no-cache"

    return resp


@flask.current_app.route("/static/img/<filename>")
def get_image(filename: str):
    return flask.send_from_directory(
        os.path.join(flask.current_app.root_path, "static", "img"), filename
    )

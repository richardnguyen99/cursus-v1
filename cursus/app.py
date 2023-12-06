# -*- coding: utf-8 -*-

"""Cursus app factory module
"""

import os
import flask
import datetime

from flask import Flask
from flask_assets import Bundle
from webassets.bundle import get_filter
from flask_login import logout_user, login_required
from logging.config import dictConfig

from .apis import api_bp as api_bp_v1
from .views import view_bp, oauth_bp
from .util.extensions import db, migrate, ma, login_manager, assets, cache
from .models import User, ActiveToken


if os.environ.get("FLASK_ENV") != "development":
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s >>> %(message)s",
                    "datefmt": "%Y-%m-%dT%H:%M:%SZ",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "size-rotate": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "cursus.log",
                    "maxBytes": 1024 * 1024 * 5,
                    "backupCount": 5,
                    "formatter": "default",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", "size-rotate"],
            },
        }
    )


def create_app() -> Flask:
    """App factory function to create a Flask app instance

    The pattern is carefully described in the Flask documentation

    :see https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
    """

    # Create a Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration for the application
    app.config.from_object(os.environ.get("APP_SETTINGS"))

    # Register Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    assets.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)

    with app.app_context():
        login_manager.login_view = "views.show"
        login_manager.session_protection = "strong"

        scss_bundle = Bundle(
            "scss/global.scss",
            filters="scss,autoprefixer6,cssmin",
            output="css/min.bundle.css",
            # https://webassets.readthedocs.io/en/latest/bundles.html#bundles
            depends="scss/**/_*.scss",
        )

        babel_filter = get_filter(
            "babel",
            presets=app.config["BABEL_PRESET_ENV_PATH"],
        )

        js_bundle = Bundle(
            "js/app.js",
            "js/dropdown.js",
            "js/index.js",
            "js/profile.js",
            output="js/min.bundle.js",
            filters=(babel_filter, "uglifyjs"),
            depends="js/**/*",
        )

        assets.register("css_all", scss_bundle)
        assets.register("js_all", js_bundle)

    @login_manager.user_loader
    def load_user(id):
        user_with_token = (
            db.session.query(ActiveToken.token, User)
            .select_from(User)
            .outerjoin(ActiveToken, User.id == ActiveToken.user_id)
            .filter(User.id == id)
            .first()
        )

        # The above query returns a tuple of an API token and a User object
        # However, Flask-Login expects a User object, so we have to set the
        # active token manually
        user_with_token[1].active_token = user_with_token[0]

        return user_with_token[1]

    @login_manager.unauthorized_handler
    def handle_needs_login():
        flask.flash("You have to be logged in to access this page.")
        return flask.redirect(
            flask.url_for("views.login", next=flask.request.endpoint)
        )

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return flask.redirect(flask.url_for("views.show", page_name="index"))

    # Register views
    app.register_blueprint(api_bp_v1)
    app.register_blueprint(view_bp)
    app.register_blueprint(oauth_bp)

    @app.route("/ping")
    def ping():
        resp = flask.make_response(flask.json.dumps({"message": "pong"}), 200)
        resp.headers["Content-Type"] = "application/json"

        return resp

    @app.route("/sw.js")
    def sw():
        resp = flask.make_response(
            flask.send_from_directory("static", "sw.js"), 200
        )
        resp.headers["Content-Type"] = "application/javascript"
        resp.headers["Cache-Control"] = "no-cache"

        return resp

    @app.route("/robots.txt")
    def robots():
        resp = flask.make_response(
            flask.send_from_directory("static", "robots.txt"), 200
        )
        resp.headers["Content-Type"] = "text/plain"
        resp.headers["Cache-Control"] = "no-cache"

        return resp

    @app.after_request
    def after(response: flask.Response):
        current_app = flask.current_app
        req = flask.request

        current_app.logger.info(
            f'"{req.remote_addr}" {req.method} {req.path} \
{response.status_code} {response.content_length}'
        )

        if req.path.startswith("/static"):
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
                return response.make_conditional(req)

            response.headers["Cache-Control"] = "public, max-age=31536000"

            return response.make_conditional(req)

        return response

    @app.teardown_appcontext
    def shutdown_session(exception=None):  # pylint: disable=unused-argument
        db.session.remove()

    return app

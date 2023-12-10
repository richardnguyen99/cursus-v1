# -*- coding: utf-8 -*-

"""Cursus app factory module
"""

import os

from flask import Flask
from logging.config import dictConfig


from .apis import api_bp as api_bp_v1
from .views import view_bp, oauth_bp
from .util.extensions import db, migrate, ma, login_manager, assets, cache


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

    # Register blueprints
    app.register_blueprint(api_bp_v1)
    app.register_blueprint(view_bp)
    app.register_blueprint(oauth_bp)

    # Register after request functions
    from .requests import after

    app.after_request(after)

    with app.app_context():
        login_manager.login_view = "views.show"
        login_manager.session_protection = "strong"

        # Register general routes
        from .routes import logout, ping, sw, robots, get_image

        from .swagger import swagger_blueprint

        app.register_blueprint(swagger_blueprint())

        from .assets import scss_bundle, js_bundle

        assets.register("css_all", scss_bundle)
        assets.register("js_all", js_bundle)

        from .context import (
            inject_content_hash,
            shutdown_session,
            load_user,
            handle_needs_login,
        )

        login_manager.user_loader(load_user)
        login_manager.unauthorized_handler(handle_needs_login)

        app.teardown_appcontext(shutdown_session)
        app.context_processor(inject_content_hash)

    return app

# -*- coding: utf-8 -*-

"""Cursus general context handlers module

This submodule contains context handlers for general purposes such as managing
the user session and the application context.
"""

import os
import flask

from .models import User, ActiveToken
from .util import generate_content_hash
from .util.extensions import db


def load_user(id):
    """Load a user from the database"""

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


def handle_needs_login():
    flask.flash("You have to be logged in to access this page.")
    return flask.redirect(
        flask.url_for("views.login", next=flask.request.endpoint)
    )


def shutdown_session(exception=None):  # pylint: disable=unused-argument
    db.session.remove()


def inject_content_hash():
    def content_hash_for_image(filename):
        """Generate a content hash for cache-busting images"""

        image_path = os.path.join(
            flask.current_app.root_path, "static", "img", filename
        )
        return generate_content_hash(image_path)

    return dict(content_hash_for_image=content_hash_for_image)

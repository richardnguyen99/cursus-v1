# -*- coding: utf-8 -*-

"""List of protected endpoitns used by the Cursus application
"""

import flask

from flask_login import current_user, login_required

from . import view_bp
from cursus.util.extensions import db, cache
from cursus.models import ActiveToken
from cursus.util import exceptions


@view_bp.route("/profile/revoke_token", methods=["GET"])
def profile_revoke():
    """Revoke an API token from the current user"""

    if not current_user.is_authenticated:
        return (
            flask.json.jsonify(
                {
                    "type": "error",
                    "message": "You must be logged in to revoke an API token",
                }
            ),
            401,
        )

    req = flask.request

    if req.method != "GET" and req.method != "HEAD":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    old_token = (
        db.session.query(ActiveToken)
        .filter_by(user_id=current_user.id)
        .first()
    )

    if old_token:
        db.session.delete(old_token)
        db.session.commit()

        cache.set(old_token.token, False, timeout=60 * 60 * 24 * 7)

        revoked_token = cache.get(old_token.token)

        return (
            flask.json.jsonify(
                {
                    "type": "success",
                    "message": "Token revoked",
                    "data": {
                        "token": old_token.token,
                        "active": revoked_token,
                    },
                }
            ),
            200,
        )

    return (
        flask.json.jsonify({"type": "info", "message": "No token found"}),
        200,
    )


@view_bp.route("/profile/generate_token", methods=["GET"])
def profile_generate():
    """Generate an API token for the current user"""

    if not current_user.is_authenticated:
        return (
            flask.json.jsonify(
                {"message": "You must be logged in to generate an API token"}
            ),
            401,
        )

    req = flask.request

    if req.method != "GET" and req.method != "HEAD":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    token = ActiveToken(
        token=ActiveToken.generate_token(),
        user_id=current_user.id,
    )

    cached_token = cache.get(token.token)

    # Check if revoked token exists in the cache and generate a new one if does
    while cached_token and cached_token == False:
        token.token = ActiveToken.generate_token()
        cached_token = cache.get(token.token)

    old_token = (
        db.session.query(ActiveToken)
        .filter_by(user_id=current_user.id)
        .first()
    )

    # Delete the old token if exists
    if old_token:
        db.session.delete(old_token)
        db.session.commit()

        cache.set(old_token.token, False, timeout=60 * 60 * 24 * 7)

    # Commit the token to the database
    db.session.add(token)
    db.session.commit()

    return (
        flask.json.jsonify(
            {
                "id": current_user.id,
                "active_token": str(token),
                "revoked_token": str(old_token),
            }
        ),
        200,
    )


@view_bp.route("/profile", methods=["GET"])
@view_bp.route("/profile/", methods=["GET"])
@login_required
def profile():
    return flask.redirect(
        flask.url_for("views.profile_account", sub_page="account")
    )


@view_bp.route("/profile/<sub_page>")
def profile_account(sub_page: str):
    if not current_user.is_authenticated:
        return flask.redirect(flask.url_for("views.profile"))

    req = flask.request

    if req.method != "GET" and req.method != "HEAD":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    content = flask.render_template(
        f"profile-{sub_page}.html",
        user_id=current_user.id,
        active_token=current_user.token,
    )

    if "X-Requested-SPA" in req.headers:
        resp = flask.make_response(content, 200)
        resp.headers["X-Response-SPA"] = "true"
    else:
        resp = flask.make_response(
            flask.render_template(
                "_profile.html",
                page_name="profile",
            )
        )

    return resp, 200

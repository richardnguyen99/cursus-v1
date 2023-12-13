# -*- coding: utf-8 -*-

"""List of protected endpoitns used by the Cursus application
"""

import flask
import json
import datetime
import sqlalchemy as sa

from flask_login import current_user, login_required
from sqlalchemy.sql import func

from . import view_bp
from cursus.util.extensions import db, cache
from cursus.models import ActiveToken, History, Account
from cursus.schema.history import HistorySchema
from cursus.util import exceptions, datetime as cursus_datetime


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
        history_log = History(
            user_id=current_user.id, type="revoke", token_used=old_token.token
        )

        db.session.delete(old_token)
        db.session.flush()

        db.session.add(history_log)
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
        if "Referer" not in flask.request.headers:
            return flask.redirect(
                flask.url_for(
                    "views.login",
                )
            )

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

    num_generated_token = cache.get(f"{current_user.id}-generatedTime")

    if num_generated_token is not None:
        item = json.loads(num_generated_token)

        if item["generatedTime"] >= 5:
            return (
                flask.json.jsonify(
                    {
                        "type": "error",
                        "message": "\
You have reached the maximum number of tokens generated per day",
                    }
                ),
                403,
            )

        item["generatedTime"] += 1

        # Compute time to live until the end of the day
        created_time = datetime.datetime.strptime(
            item["created_at"], "%a, %d %b %Y %H:%M:%S GMT"
        )
        ttl = cursus_datetime.datetime_until_end_of_day(created_time)

        cache.set(
            f"{current_user.id}-generatedTime",
            json.dumps(item),
            timeout=ttl.seconds,
        )

    # If the cache key doesn't exist, i.e. the user hasn't generated any token
    # today
    else:
        generatedTime = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )

        item = {
            "generatedTime": 1,
            "created_at": generatedTime,
        }

        cache.set(
            f"{current_user.id}-generatedTime",
            json.dumps(item),
            timeout=cursus_datetime.datetime_until_end_of_day().seconds,
        )

    token = ActiveToken(
        token=ActiveToken.generate_token(),
        user_id=current_user.id,
    )

    history = History(
        user_id=current_user.id,
        type="generate",
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
    db.session.flush()

    # https://stackoverflow.com/questions/620610/sqlalchemy-obtain-primary-key-with-autoincrement-before-commit
    history.token_used = token.token
    db.session.add(history)
    db.session.commit()

    return (
        flask.json.jsonify(
            {
                "id": current_user.id,
                "message": "Token generated successfully",
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
        flask.url_for(
            "views.profile_account",
            sub_page="account",
        )
    )


SUPPORT_PROFILE_SUB_PAGES = (
    "account",
    "token",
    "history",
)


@view_bp.route("/profile/<sub_page>")
def profile_account(sub_page: str):
    if not current_user.is_authenticated:
        return flask.redirect(flask.url_for("views.profile"))

    if sub_page not in SUPPORT_PROFILE_SUB_PAGES:
        raise exceptions.NotFoundError(f"Page {sub_page} not found")

    req = flask.request

    if req.method != "GET" and req.method != "HEAD":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    content_dict = {
        "user_id": current_user.id,
        "active_token": current_user.token,
    }

    if sub_page == "history":
        # """
        # SELECT T.token, H.*
        # FROM history as H
        # LEFT JOIN active_tokens as T
        #   ON H.token_id = T.id
        # WHERE H.user_id = id
        #   ORDER BY H."at" DESC;
        # """

        history_logs = reversed(
            db.session.query(
                History.token_used.label("token"),
                History.type,
                func.to_char(
                    History.at,
                    "Mon DD, YYYY at HH12:MI PM",
                ).label("at"),
            )
            .select_from(History)
            .outerjoin(ActiveToken, History.token_used == ActiveToken.token)
            .filter(History.user_id == current_user.id)
            .all()
        )

        content_dict["logs"] = history_logs

    content = flask.render_template(
        f"profile-{sub_page}.html",
        **content_dict,
    )

    if "X-Requested-SPA" in req.headers:
        resp = flask.make_response(content, 200)
        resp.headers["X-Response-SPA"] = "true"
    else:
        resp = flask.make_response(
            flask.render_template(
                "_profile.html",
                page_name="profile",
                current_user=current_user,
            )
        )

    return resp, 200

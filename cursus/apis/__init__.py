# -*- coding: utf-8 -*-

"""Cursus core view module

This module contains API endpoints for the Cursus application.
"""

import flask
import datetime
import json

from flask import Blueprint, jsonify, request
from werkzeug import exceptions as WerkzeugExceptions

from cursus.models import ActiveToken
from cursus.util import CursusException
from cursus.util.extensions import cache, db
from cursus.util.datetime import datetime_until_end_of_day

from .university import (
    university_find,
    university_index,
    university_get_by_name,
)


api_bp: Blueprint = Blueprint(
    name="api", import_name=__name__, url_prefix="/api/v1/university"
)

api_bp.add_url_rule("/", "index", view_func=university_index)
api_bp.add_url_rule(
    "/find", "find", view_func=university_find, methods=["GET", "POST"]
)
api_bp.add_url_rule(
    "/<name>",
    "api_name",
    view_func=university_get_by_name,
)


@api_bp.before_request
def before_request():
    if "X-CURSUS-API-TOKEN" not in request.headers:
        raise CursusException.BadRequestError(
            "API endpoints require an authorized API token"
        )

    token = request.headers["X-CURSUS-API-TOKEN"]
    token_from_cache = cache.get(token)

    if token_from_cache and token_from_cache is False:
        raise CursusException.UnauthorizedError("Invalid API Token")

    cache_item = json.loads(token_from_cache)

    if token_from_cache:
        if "request_count" in cache_item and cache_item["request_count"] >= 50:
            raise CursusException.UnauthorizedError(
                "API Token rate limit exceeded"
            )

        return None

    # No token is found from cache, so we need to check if there is one in db
    token_from_db = (
        db.session.query(ActiveToken).filter_by(token=token).first()
    )

    if token_from_db is None:
        raise CursusException.UnauthorizedError("Invalid API Token")

    cache_item = {
        "token": token_from_db.token,
        "user_id": token_from_db.user_id,
        "created": datetime.datetime.utcnow().strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        ),
        "request_count": 0,
    }

    # Cache rate limit for one day (in seconds)
    cache.set(token, json.dumps(cache_item), timeout=60 * 60 * 24)


@api_bp.after_request
def after_request(response: flask.Response):
    response.headers["Content-Type"] = "application/json"

    if response.status_code != 200:
        return response

    token = request.headers["X-CURSUS-API-TOKEN"]
    cache_item = cache.get(token)

    if cache_item is None:
        raise CursusException.InternalServerError(
            "Cache item not found after processing request"
        )

    cache_item = json.loads(cache_item)
    cache_item["request_count"] += 1

    created_time = datetime.datetime.strptime(
        cache_item["created"], "%a, %d %b %Y %H:%M:%S GMT"
    )

    ttl = datetime_until_end_of_day(created_time)

    cache.set(token, json.dumps(cache_item), timeout=ttl.seconds)

    return response


@api_bp.errorhandler(WerkzeugExceptions.HTTPException)
def handle_http_error(error: WerkzeugExceptions.HTTPException):
    return (
        jsonify(
            {
                "error": {
                    "code": error.code,
                    "message": error.description,
                    "reason": error.name,
                }
            }
        ),
        error.code,
    )


@api_bp.errorhandler(CursusException.CursusError)
def handle_api_error(error: CursusException.CursusError):
    return (
        jsonify(
            {
                "error": {
                    "code": error.status_code,
                    "message": error.status_msg,
                    "reason": error.reason,
                }
            }
        ),
        error.status_code,
    )

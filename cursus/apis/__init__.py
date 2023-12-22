# -*- coding: utf-8 -*-

"""Cursus core view module

This module contains API endpoints for the Cursus application.
"""

import flask
import datetime
import json
import os

from flask import Blueprint, jsonify, request
from werkzeug import exceptions as WerkzeugExceptions

from cursus.models import ActiveToken
from cursus.util import CursusException
from cursus.util.extensions import cache, db

from .search import (
    search_university,
    search_school,
    search_department,
    search_course,
)
from .school import (
    school_by_id,
)
from .university import (
    university_find,
    university_index,
    university_get_by_name,
)


def check_preflight_request(request: flask.Request) -> bool:
    """Check if the request is a preflight request

    A preflight request is a CORS request that checks if the API endpoint is
    allowed to be accessed outside of the domain. This function checks if the
    request is a preflight request by checking if the request method is OPTIONS
    and if the request headers contain the `Origin` header.

    Args:
        request (flask.Request): The request object

    Returns:
        bool: True if the request is a preflight request, False otherwise
    """

    if "Origin" not in request.headers:
        return False

    if "Access-Control-Request-Method" not in request.headers:
        return False

    if request.headers["Access-Control-Request-Method"] != "GET":
        return False

    if "Access-Control-Request-Headers" not in request.headers:
        return False

    if (
        "x-cursus-api-token"
        != request.headers["Access-Control-Request-Headers"].lower()
    ):
        return False

    return True


def make_cors_headers(response: flask.Response) -> flask.Response:
    """Make CORS headers for the response

    Args:
        response (flask.Response): The response object

    Returns:
        flask.Response: The response object with CORS headers
    """

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Headers",
        "X-CURSUS-API-TOKEN, Accept, Origin",
    )
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Max-Age", "86400")

    return response


api_bp: Blueprint = Blueprint(
    name="api", import_name=__name__, url_prefix="/api/v1/"
)

search_bp: Blueprint = Blueprint(
    name="search", import_name=__name__, url_prefix="/search/"
)

university_bp: Blueprint = Blueprint(
    name="university", import_name=__name__, url_prefix="/university/"
)

school_bp: Blueprint = Blueprint(
    name="school", import_name=__name__, url_prefix="/school/"
)

###############################################################################
#                                                                             #
#                                 Search API                                  #
#                                                                             #
###############################################################################

search_bp.add_url_rule(
    "/university", "university", view_func=search_university
)

search_bp.add_url_rule("/school", "school", view_func=search_school)

search_bp.add_url_rule(
    "/department", "department", view_func=search_department
)

search_bp.add_url_rule("/course", "course", view_func=search_course)

###############################################################################
#                                                                             #
#                               University API                                #
#                                                                             #
###############################################################################

university_bp.add_url_rule("/", "index", view_func=university_index)
university_bp.add_url_rule(
    "/find", "find", view_func=university_find, methods=["GET", "POST"]
)
university_bp.add_url_rule(
    "/<name>",
    "api_name",
    view_func=university_get_by_name,
)

###############################################################################
#                                                                             #
#                                 School API                                  #
#                                                                             #
###############################################################################

school_bp.add_url_rule(
    "/<int:id>", "id", view_func=school_by_id, methods=["GET"]
)


@api_bp.route("/<path:path>", methods=["GET"])
def not_found(path: str):
    """Return a 404 response for all unknown API endpoints"""

    raise WerkzeugExceptions.NotFound(
        description=f"API endpoint, {path}, not found"
    )


@api_bp.route("/swagger.json", methods=["GET"])
def swagger():
    """Return the Swagger API specification file from swagger.json"""

    swagger_path = os.getcwd() + "/cursus/apis/swagger.json"
    swagger_file = open(swagger_path, "r")
    swagger_json = json.load(swagger_file)

    swagger_file.close()

    return jsonify(swagger_json)


@api_bp.before_request
def before_request():
    """Process actions all requests that are made to the API endpoints"""

    if request.path.endswith("/swagger.json"):
        return None

    if request.method != "OPTIONS" and request.method != "GET":
        raise CursusException.MethodNotAllowedError(
            "Only GET requests are allowed"
        )

    # Prelight request to check if the API endpoint is allowed to be accessed
    # outside of the domain
    if request.method == "OPTIONS":
        if check_preflight_request(request):
            # Returning a non-None value from a before_request handler will
            # cause Flask to skip the normal request handling and continue to
            # the after request handler.
            return flask.make_response()

        raise CursusException.BadRequestError("Invalid preflight request")

    # Missing API token
    if "X-CURSUS-API-TOKEN" not in request.headers:
        raise CursusException.BadRequestError(
            "API endpoints require an authorized API token"
        )

    token = request.headers["X-CURSUS-API-TOKEN"]
    token_from_cache = cache.get(token)

    # Token is found from cache but it's blacklisted
    if token_from_cache == False:
        raise CursusException.UnauthorizedError("Invalid API Token")

    # Token is found from cache and it's not revoked
    if token_from_cache:
        cache_item = json.loads(token_from_cache)

        if "request_count" in cache_item and cache_item["request_count"] >= 50:
            raise CursusException.ForbiddenError(
                "API Token rate limit exceeded"
            )

        return None

    # No token is found from cache, so we need to check if there is one in db
    token_from_db = (
        db.session.query(ActiveToken).filter_by(token=token).first()
    )

    if token_from_db is None:
        raise CursusException.UnauthorizedError("Invalid API Token")

    now = datetime.datetime.utcnow()

    cache_item = {
        "token": token_from_db.token,
        "user_id": token_from_db.user_id,
        "created": now.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "expired": (now + datetime.timedelta(minutes=60)).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        ),
        "request_count": 0,
    }

    # Cache rate limit for one hour (in seconds)
    cache.set(token, json.dumps(cache_item), timeout=60 * 60)


@api_bp.after_request
def after_request(response: flask.Response):
    """Perform actions after a request has been processed"""

    if request.path.endswith("/swagger.json"):
        return response

    make_cors_headers(response)

    # A response that made it to the endpoint handler either succeeded (200) or
    # failed (404) to retrieve the requested resource. In both cases, we want
    # to increment the request count for the API token.
    #
    # Other HTTP status codes are already handled by the error handlers.
    if response.status_code != 200 and response.status_code != 404:
        return response

    if request.method == "OPTIONS":
        return response

    token = request.headers["X-CURSUS-API-TOKEN"]
    cache_item = cache.get(token)

    cache_obj = json.loads(cache_item)
    cache_obj["request_count"] += 1

    # Compute the time to live up to one day starting from the time the token
    # was first created.

    expired_time = datetime.datetime.strptime(
        cache_obj["expired"], "%a, %d %b %Y %H:%M:%S GMT"
    )

    ttl = expired_time - datetime.datetime.utcnow()

    if ttl.seconds < 0:
        ttl = datetime.timedelta(minutes=60)

    cache.set(token, json.dumps(cache_obj), timeout=ttl.seconds)

    response.headers.add("X-Cursus-Limit", "50")
    response.headers.add(
        "X-Cursus-Remaining", str(50 - cache_obj["request_count"])
    )
    response.headers.add("X-Cursus-Start", cache_obj["created"])
    response.headers.add("X-Cursus-TTL", str(ttl.seconds))

    return response


@api_bp.errorhandler(WerkzeugExceptions.NotFound)
def handle_api_not_found(error: WerkzeugExceptions.NotFound):
    """Handle API 404 errors"""

    resp = flask.make_response(
        jsonify(
            {
                "error": {
                    "code": 404,
                    "message": "Not Found",
                    "reason": "NOT_FOUND",
                }
            }
        ),
        404,
    )

    return resp


@api_bp.errorhandler(WerkzeugExceptions.HTTPException)
def handle_http_error(error: WerkzeugExceptions.HTTPException):
    """Handle generic Werkzeug HTTP exceptions"""

    resp = flask.make_response(
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

    return resp


@api_bp.errorhandler(CursusException.CursusError)
def handle_api_error(error: CursusException.CursusError):
    """Handle generic Cursus API exceptions

    When an API endpoint raises a `CursusError`, which accepts all status codes
    as an argument, this error handler will return a JSON response with the
    error code, message, and reason.
    """
    resp = flask.make_response(
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

    return resp


api_bp.register_blueprint(search_bp)
api_bp.register_blueprint(university_bp)
api_bp.register_blueprint(school_bp)

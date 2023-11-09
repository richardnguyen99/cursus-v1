# -*- coding: utf-8 -*-

"""Cursus core view module

This module contains API endpoints for the Cursus application.
"""

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed

from cursus.util import CursusException

from .find import find_index, find_university
from .university import (
    university_index,
    university_find,
    university_get_by_name,
)


find_bp: Blueprint = Blueprint("find", __name__, url_prefix="/find")
find_bp.add_url_rule("/", "index", view_func=find_index)
find_bp.add_url_rule(
    "/<university_name>", "university_name", view_func=find_university
)

university_bp: Blueprint = Blueprint(
    name="university", import_name=__name__, url_prefix="/api/v1/university"
)

university_bp.add_url_rule("/", "index", view_func=university_index)
university_bp.add_url_rule(
    "/find", "find", view_func=university_find, methods=["GET", "POST"]
)
university_bp.add_url_rule(
    "/<name>",
    "university_name",
    view_func=university_get_by_name,
)


@university_bp.app_errorhandler(CursusException.BadRequestError)
@university_bp.app_errorhandler(BadRequest)
@university_bp.app_errorhandler(400)
def handle_bad_request(error: CursusException.BadRequestError):
    if type(error) is int and error == 400:
        return jsonify({"message": f"{request.url}: Bad Request"}), 400
    elif isinstance(error, BadRequest):
        return jsonify({"message": error.get_description()}), 400

    return jsonify({"message": error.get_reason()}), 400


@university_bp.app_errorhandler(CursusException.NotFoundError)
@university_bp.app_errorhandler(NotFound)
@university_bp.app_errorhandler(404)
def handle_not_found(error: CursusException.NotFoundError | NotFound | int):
    if type(error) is int and error == 404:
        return jsonify({"message": f"{request.url}: Not Found"}), 404
    elif isinstance(error, NotFound):
        return jsonify({"message": error.get_description()}), 404

    return jsonify({"message": error.get_reason()}), 404


@university_bp.app_errorhandler(CursusException.MethodNotAllowedError)
@university_bp.app_errorhandler(MethodNotAllowed)
@university_bp.app_errorhandler(405)
def handle_method_not_allowed(
    error: CursusException.MethodNotAllowedError | MethodNotAllowed | int,
):
    if type(error) is int and error == 405:
        return jsonify({"message": f"{request.url}: Method Not Allowed"}), 405
    elif isinstance(error, MethodNotAllowed):
        return jsonify({"message": error.get_description()}), 405

    return jsonify({"message": error.get_reason()}), 405

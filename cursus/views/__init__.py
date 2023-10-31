# -*- coding: utf-8 -*-

"""Cursus core view module

This module contains API endpoints for the Cursus application.
"""

from flask import Blueprint

from .find import find_index, find_university

find_bp: Blueprint = Blueprint("find", __name__, url_prefix="/find")
find_bp.add_url_rule("/", "index", view_func=find_index)
find_bp.add_url_rule(
    "/<university_name>", "university_name", view_func=find_university
)

# -*- coding: utf-8 -*-

"""
School API endpoint handlers
"""

import urllib
import flask

from cursus.schema import SchoolSchema
from cursus.models import School, University
from cursus.util import CursusException
from cursus.util.extensions import db
from cursus.util.requests import (
    get_parsed_dict,
    has_require_params,
    get_limit,
)


def school_find():
    """School find endpoint with query string"""

    req = flask.request

    parsed_dict = get_parsed_dict(req.query_string.decode("utf-8"))

    if not parsed_dict:
        raise CursusException.BadRequestError(
            "Query string cannot be empty while using this endpoint"
        )

    if not has_require_params(parsed_dict, ["name"]):
        raise CursusException.BadRequestError(
            "Query string must contain a `name` argument"
        )

    try:
        limit = get_limit(parsed_dict)
    except Exception as e:
        raise CursusException.BadRequestError(str(e))

    search_string = parsed_dict["name"]

    schools = (
        db.session.query(
            *School.__table__.columns,
            University.full_name.label("university_full_name"),
            University.short_name.label("university_short_name"),
        )
        .select_from(School)
        .join(University, School.university_id == University.id)
        .filter(School.name.ilike(f"%{search_string}%"))
        .limit(limit)
    )

    only_fields = (
        "id",
        "name",
        "university_full_name",
        "university_short_name",
    )

    school_schema = SchoolSchema(only=only_fields)

    resp = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "count": schools.count(),
                "data": school_schema.dump(schools, many=True),
            }
        )
    )

    resp.mimetype = "application/json"

    return resp, 200


def school_by_short_name(short_name: str):
    """Get a school by its short name"""

    req = flask.request
    dump_fields = {
        "id": True,
        "name": True,
        "website": True,
        "created_at": True,
        "modified_at": True,
        "departments": False,
        "university": False,
    }

    parsed_dict = get_parsed_dict(req.query_string.decode("utf-8"))

    university = (
        db.session.query(University).filter_by(short_name=short_name).first()
    )

    if not university:
        raise CursusException.NotFoundError(
            "University by short name not found"
        )

    schools = (
        db.session.query(School).filter_by(university_id=university.id).all()
    )

    if (
        parsed_dict
        and "showDeps" in parsed_dict
        and parsed_dict["showDeps"] == "true"
    ):
        dump_fields["departments"] = True

    only_fields = tuple([key for key, value in dump_fields.items() if value])

    resp = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "count": len(schools),
                "university": university.full_name,
                "code": university.short_name,
                "data": SchoolSchema(many=True, only=only_fields).dump(
                    schools
                ),
            }
        )
    )

    resp.mimetype = "application/json"

    return resp, 200

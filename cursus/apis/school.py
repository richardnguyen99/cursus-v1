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


def school_find():
    """School find endpoint with query string"""

    req = flask.request

    # Get request query string
    query_string = req.query_string.decode("utf-8")

    # Check if query string is empty
    if not query_string:
        reason = "Query string cannot be empty while using this endpoint"
        raise CursusException.BadRequestError(reason)

    # Parse query string into a dictionary of arguments
    query_dict = urllib.parse.parse_qs(query_string)

    # parse_qs returns a list of values for each key. This will convert the
    # list into a single value.
    parsed_dict = {key: value[0] for key, value in query_dict.items()}

    if "name" not in parsed_dict or not parsed_dict["name"]:
        reason = "Query string must contain a `name` argument"
        raise CursusException.BadRequestError(reason)

    limit = 5

    if "limit" in parsed_dict and parsed_dict["limit"]:
        try:
            limit_from_query = int(parsed_dict["limit"])

            if limit_from_query > 0:
                limit = min(limit_from_query, 10)
            else:
                reason = "`limit` argument must be greater than 0"
                raise CursusException.BadRequestError(reason)
        except ValueError:
            reason = "`limit` argument must be an integer"
            raise CursusException.BadRequestError(reason)

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

# -*- coding: utf-8 -*-

"""
School API endpoint handlers
"""

import flask
import sqlalchemy as sa

from cursus.schema import SchoolSchema
from cursus.models import School, University, Department
from cursus.util import CursusException
from cursus.util.extensions import db


def school_by_id(id: int):
    """Get a school by its short name"""

    req = flask.request

    show_departments = req.args.get("showDeps", "false").lower() == "true"

    dump_fields = {
        "id": True,
        "name": True,
        "university_id": True,
        "website": True,
        "created_at": True,
        "modified_at": True,
        "departments": False,
        "total_departments": True,
    }

    school = (
        db.session.query(
            School,
            sa.func.coalesce(sa.func.count(Department.id), 0).label(
                "total_departments"
            ),
        )
        .outerjoin(Department, full=True)
        .group_by(School.id)
        .filter(
            School.id == id,
        )
        .first()
    )

    if show_departments:
        dump_fields["departments"] = True

    if school is not None:
        print(school)
        school[0].total_departments = school[1]

    only_fields = tuple([key for key, value in dump_fields.items() if value])
    school_schema = SchoolSchema(only=only_fields)

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "Success" if school else "Not found",
                "result": school_schema.dump(school[0] if school else None),
            }
        )
    )

    response.mimetype = "application/json"

    return response, 200

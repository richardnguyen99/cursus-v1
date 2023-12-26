# -*- coding: utf-8 -*-

"""
School API endpoint handlers
"""

import flask
import sqlalchemy as sa

from cursus.schema import SchoolSchema
from cursus.models import School, Department
from cursus.util.extensions import db


def _map_school_with_count(school):
    if school is None:
        return None

    school[0].total_departments = school[1]
    return school[0]


def schools_by_univeristy_id(university_id: int):
    "Get a list of schools in a university"

    req = flask.request

    page = req.args.get("page", 1, type=int)
    sort_by = req.args.get("sort_by", None, type=str)

    dump_fields = (
        "id",
        "name",
        "website",
        "created_at",
        "modified_at",
        "total_departments",
    )

    schools = (
        db.session.query(
            School,
            sa.func.coalesce(sa.func.count(Department.id), 0).label(
                "total_departments"
            ),
        )
        .outerjoin(Department, full=True)
        .group_by(School.id)
        .filter(
            School.university_id == university_id,
        )
    )

    if sort_by:
        if sort_by == "name":
            schools = schools.order_by(School.name)
        elif sort_by == "depnum":
            schools = schools.order_by(sa.desc("total_departments"))

    if schools is None:
        return flask.make_response(
            flask.jsonify(
                {
                    "message": "Not found",
                    "results": [],
                }
            ),
            200,
        )

    school_schema = SchoolSchema(only=dump_fields)

    school_page = schools.paginate(page=page, per_page=10, error_out=True)

    school_page.items = list(map(_map_school_with_count, school_page.items))

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "total": schools.count(),
                "page": page,
                "pages": school_page.pages,
                "university_id": university_id,
                "result": school_schema.dump(school_page, many=True),
            }
        )
    )
    response.mimetype = "application/json"

    return response, 200


def school_by_id(id: int):
    """Get a school by its short name"""

    req = flask.request

    show_departments = req.args.get("show_deps", "false").lower() == "true"

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

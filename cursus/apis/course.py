# -*- coding: utf-8 -*-

"""
Course API endpoint handlers
"""

import flask

from cursus.models import Course
from cursus.schema import CourseSchema


def _course_not_found_response(course_id):
    return flask.make_response(
        flask.jsonify(
            {
                "message": f"Course with id {course_id} not found. if you \
want to add this course, please open a pull request at \
https://github.com/richardnguyen99/cursus/pulls.",
                "result": {},
            }
        ),
        404,
    )


def _course_by_department_not_found_response(department_id):
    return flask.make_response(
        flask.jsonify(
            {
                "message": f"Course with department id {department_id} is not \
found. If you want to add this course, please open a pull request at \
https://github.com/richardnguyen99/cursus/pulls.",
                "result": [],
            }
        ),
        404,
    )


def course_by_id(course_id: int):
    """Get course information by course id"""

    req = flask.request

    dump_fields = (
        "id",
        "title",
        "code",
        "website",
        "active",
        "level",
        "subject",
        "modified_at",
        "created_at",
        "department_id",
        "university_id",
        "description",
        "credits",
    )

    courses = Course.query.filter(Course.id == course_id).first()

    if courses is None:
        return _course_not_found_response(course_id)

    course_schema = CourseSchema(only=dump_fields)

    return flask.make_response(
        flask.jsonify(
            {
                "message": f"Course with id {course_id} found.",
                "result": course_schema.dump(courses),
            }
        ),
        200,
    )


def courses_by_department(department_id: int):
    """Get a list of courses by a department id"""

    req = flask.request

    page = req.args.get("page", 1, type=int)
    filters = req.args.get("filters", None, type=str)

    dump_fields = (
        "id",
        "title",
        "code",
        "website",
        "active",
        "level",
        "subject",
        "modified_at",
        "created_at",
        "university_id",
        "description",
        "credits",
    )

    courses = Course.query.filter(Course.department_id == department_id)

    if courses is None:
        return _course_by_department_not_found_response(department_id)

    if filters:
        filter_list = filters.strip().lower().split(",")

        for f in filter_list:
            if f == "undergraduate":
                courses = courses.filter(Course.level == 1)
            elif f == "graduate":
                courses = courses.filter(Course.level == 2)
            elif f == "active":
                courses = courses.filter(Course.active)

    course_schema = CourseSchema(many=True, only=dump_fields)

    course_page = courses.paginate(page=page, per_page=10, error_out=True)

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "success",
                "page": page,
                "total_pages": course_page.pages,
                "total_results": courses.count(),
                "results_per_page": 10,
                "department_id": department_id,
                "result": course_schema.dump(course_page, many=True),
            }
        )
    )
    response.mimetype = "application/json"

    return response, 200

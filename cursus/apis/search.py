# -*- coding: utf-8 -*-

"""
Search enpoint handlers
"""

import flask
import sqlalchemy as sa

from typing import Optional

from cursus.util.extensions import db
from cursus.schema import (
    UniversitySchema,
    SchoolSchema,
    DepartmentSchema,
    CourseSchema,
)
from cursus.models import (
    University,
    UniversityCampus,
    School,
    Department,
    Course,
)
from cursus.util.exceptions import (
    BadRequestError,
)


def _search_require_query_string(query: Optional[str]):
    if not query:
        raise BadRequestError(
            "Query string cannot be empty while using this endpoint"
        )

    if len(query) < 3:
        raise BadRequestError(
            "Query string must be at least 3 characters long"
        )

    return f"%{query}%"


def _map_item_school_search(item: tuple[School, str]):
    item[0].university_full_name = item[1]

    return item[0]


def search_university():
    """Search for universities based on their names"""

    req = flask.request

    page = req.args.get("page", 1, type=int)
    before = req.args.get("beofore", None, type=int)
    after = req.args.get("after", None, type=int)
    query = req.args.get("query", None, type=str)
    display = req.args.get("display", None, type=str)
    sort_by_year = req.args.get("sort_by_year", None, type=str)
    country_code = req.args.get("country_code", None, type=str)

    search_string = _search_require_query_string(query)

    dump_fields = {
        "id": True,
        "full_name": True,
        "short_name": True,
        "established": True,
        "homepage": True,
        "former_name": False,
        "motto": False,
        "campuses": False,
        "domains": False,
        "founders": False,
    }

    universities = University.query.filter(
        University.full_name.ilike(search_string)
    )

    if country_code:
        universities = universities.join(
            UniversityCampus,
            onclause=University.short_name
            == UniversityCampus.school_short_name,
        ).filter(UniversityCampus.country_code.ilike(country_code))

    if display:
        if display == "all":
            dump_fields["campuses"] = True
            dump_fields["domains"] = True
            dump_fields["founders"] = True
        else:
            filtered_displays = display.strip().lower().split(",")

            for filter_display in filtered_displays:
                if filter_display == "campus":
                    dump_fields["campuses"] = True
                elif filter_display == "domain":
                    dump_fields["domains"] = True
                elif filter_display == "founder":
                    dump_fields["founders"] = True

    if before is not None and after is not None:
        if before <= after:
            universities = universities.filter(
                sa.func.and_(
                    University.established >= before,
                    University.established <= after,
                )
            )
    else:
        if before is not None:
            universities = universities.filter(
                University.established >= before
            )
        elif after is not None:
            universities = universities.filter(University.established <= after)

    if sort_by_year:
        if sort_by_year == "asc":
            universities = universities.order_by(University.established.asc())
        elif sort_by_year == "desc":
            universities = universities.order_by(University.established.desc())

    only_fields = tuple([key for key, value in dump_fields.items() if value])
    university_schema = UniversitySchema(only=only_fields)

    university_page = universities.paginate(
        page=page, per_page=10, error_out=True
    )

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "total": universities.count(),
                "count": len(university_page.items),
                "page": page,
                "pages": university_page.pages,
                "results": university_schema.dump(university_page, many=True),
            }
        )
    )

    response.mimetype = "application/json"

    return response, 200


def search_school():
    """Search for schools based on their names"""

    req = flask.request

    page = req.args.get("page", 1, type=int)
    query = req.args.get("query", None, type=str)
    display = req.args.get("display", None, type=str)

    search_string = _search_require_query_string(query)

    dump_fields = {
        "id": True,
        "name": True,
        "university_full_name": True,
        "website": False,
        "created_at": False,
        "modified_at": False,
        "departments": False,
    }

    schools = (
        db.session.query(
            School,
            University.full_name.label("university_full_name"),
        )
        .select_from(School)
        .outerjoin(
            University,
        )
        .filter(School.name.ilike(search_string))
    )

    if display:
        if display == "all":
            dump_fields["website"] = True
            dump_fields["created_at"] = True
            dump_fields["modified_at"] = True
            dump_fields["departments"] = True

        else:
            filtered_displays = display.strip().lower().split(",")

            for filter_display in filtered_displays:
                if filter_display == "website":
                    dump_fields["website"] = True

                if filter_display == "departments":
                    dump_fields["departments"] = True

    only_fields = tuple([key for key, value in dump_fields.items() if value])
    school_schema = SchoolSchema(only=only_fields)
    school_page = schools.paginate(page=page, per_page=10, error_out=True)

    school_page.items = list(map(_map_item_school_search, school_page.items))

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "total": schools.count(),
                "count": len(school_page.items),
                "page": page,
                "pages": school_page.pages,
                "results": school_schema.dump(school_page, many=True),
            }
        )
    )

    response.mimetype = "application/json"

    return response, 200


def search_department():
    """Search for departments based on their names"""

    req = flask.request

    page = req.args.get("page", 1, type=int)
    query = req.args.get("query", None, type=str)
    filters = req.args.get("filters", None, type=str)
    display = req.args.get("display", None, type=str)

    search_string = _search_require_query_string(query)

    default_fields = {
        "id": True,
        "name": True,
        "code": True,
        "university_name": True,
        "university_id": True,
        "website": False,
        "created_at": False,
        "modified_at": False,
        "school_name": False,
        "school_id": False,
        "undergraduate": False,
        "graduate": False,
        "type": False,
        "special_name": False,
    }

    departments = (
        db.session.query(
            *Department.__table__.columns,
            School.name.label("school_name"),
            University.full_name.label("university_name"),
        )
        .select_from(Department)
        .join(School, onclause=School.id == Department.school_id)
        .join(University, onclause=University.id == Department.university_id)
        .filter(Department.name.ilike(search_string))
    )

    if filters:
        filter_list = filters.strip().lower().split(",")

        for f in filter_list:
            if f == "undergraduate":
                departments = departments.filter(Department.undergraduate)

            if f == "graduate":
                departments = departments.filter(Department.graduate)

            if f == "active":
                departments = departments.filter(Department.active)

    if display:
        if display == "all":
            default_fields = {key: True for key in default_fields.keys()}

        else:
            display_list = display.strip().lower().split(",")

            for d in display_list:
                if d == "website":
                    default_fields["website"] = True

                if d == "school":
                    default_fields["school_name"] = True
                    default_fields["school_id"] = True

                if d == "undergraduate":
                    default_fields["undergraduate"] = True

                if d == "graduate":
                    default_fields["graduate"] = True

                if d == "type":
                    default_fields["type"] = True

                if d == "special_name":
                    default_fields["special_name"] = True

    only_fields = tuple(
        [key for key, value in default_fields.items() if value]
    )
    department_schema = DepartmentSchema(only=only_fields)
    department_page = departments.paginate(
        page=page, per_page=10, error_out=True
    )

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "total": departments.count(),
                "count": len(department_page.items),
                "page": page,
                "pages": department_page.pages,
                "results": department_schema.dump(department_page, many=True),
            }
        )
    )

    response.mimetype = "application/json"

    return response, 200


def search_course():
    """Search courses based on their names"""

    req = flask.request

    page = req.args.get("page", 1, type=int)
    query = req.args.get("query", None, type=str)
    filters = req.args.get("filters", None, type=str)
    displays = req.args.get("display", None, type=str)
    subject = req.args.get("subject", None, type=str)
    sort_by = req.args.get("sort_by", None, type=str)
    department = req.args.get("department", None, type=int)
    university = req.args.get("university", None, type=int)

    if not query:
        raise BadRequestError(
            "Query string cannot be empty while using this endpoint"
        )

    search_string = _search_require_query_string(query)

    dump_fields = {
        "id": True,
        "title": True,
        "code": True,
        "website": False,
        "active": False,
        "description": False,
        "level": False,
        "subject": False,
        "credits": False,
        "department_id": True,
        "university_id": True,
        "department_name": True,
        "university_name": True,
        "created_at": False,
        "modified_at": False,
    }

    courses = (
        db.session.query(
            *Course.__table__.c,
            Department.name.label("department_name"),
            University.full_name.label("university_name"),
        )
        .select_from(Course)
        .join(Department, onclause=Department.id == Course.department_id)
        .join(University, onclause=University.id == Department.university_id)
        .filter(Course.title.ilike(search_string))
    )

    if department:
        courses = courses.filter(Course.department_id == department)

    if university:
        courses = courses.filter(Department.university_id == university)

    if filters:
        filter_list = filters.strip().lower().split(",")

        for f in filter_list:
            if f == "active":
                courses = courses.filter(Course.active)

            if f == "undergrad":
                courses = courses.filter(Course.level == 1)

            if f == "grad":
                courses = courses.filter(Course.level == 2)

            if f == "doctorate":
                courses = courses.filter(Course.level == 3)

    if sort_by:
        if sort_by == "credits":
            courses = courses.order_by(Course.credits.desc())
        elif sort_by == "code":
            courses = courses.order_by(Course.code.asc())

    if subject:
        courses = courses.filter(Course.subject.ilike(f"%{subject}%"))

    if displays:
        if displays == "all":
            dump_fields = {key: True for key in dump_fields.keys()}
        else:
            display_list = displays.strip().lower().split(",")

            for d in display_list:
                if d in dump_fields.keys():
                    dump_fields[d] = True

    only_fields = tuple([key for key, value in dump_fields.items() if value])
    course_page = courses.paginate(page=page, per_page=10, error_out=True)
    course_schema = CourseSchema(only=only_fields)

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "total": courses.count(),
                "count": len(course_page.items),
                "page": page,
                "pages": course_page.pages,
                "results": course_schema.dump(course_page, many=True),
            }
        )
    )

    return response, 200

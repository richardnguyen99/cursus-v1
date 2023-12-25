# -*- coding: utf-8 -*-

"""
Department API endpoint handlers
"""

import flask as fl

from cursus.models import Department
from cursus.schema import DepartmentSchema


def _department_not_found_response(department_id):
    return fl.make_response(
        fl.jsonify(
            {
                "message": f"Department with id {department_id} not found. if you \
want to add this department, please open a pull request at \
https://github.com/richardnguyen99/cursus/pulls.",
                "result": {},
            }
        ),
        404,
    )


def department_by_id(department_id: int):
    """Get department information by department id"""

    req = fl.request

    department = Department.query.filter(
        Department.id == department_id
    ).first()

    if department is None:
        return _department_not_found_response(department_id)

    dump_fields = (
        "id",
        "name",
        "code",
        "website",
        "undergraduate",
        "graduate",
        "active",
        "special_name",
        "created_at",
        "modified_at",
        "university_id",
        "school_id",
    )

    department_schema = DepartmentSchema(only=dump_fields)

    res = fl.make_response(
        fl.jsonify(
            {
                "message": "success",
                "result": department_schema.dump(department),
            }
        )
    )

    res.mimetype = "application/json"

    return res, 200


def departments_by_university_id(university_id: int):
    """Get department information by university id"""

    req = fl.request

    page = req.args.get("page", default=1, type=int)
    school_id = req.args.get("school_id", default=None, type=str)
    filter = req.args.get("filter", default=None, type=str)

    departments = Department.query.filter(
        Department.university_id == university_id
    )

    if departments is None:
        return _department_not_found_response(university_id)

    if school_id is not None:
        departments = departments.filter(Department.school_id == school_id)

    if filter is not None:
        if filter == "undergrad":
            departments = departments.filter(Department.undergraduate)
        elif filter == "grad":
            departments = departments.filter(Department.graduate)

    dump_fields = {
        "id": True,
        "full_name": True,
        "code": True,
        "website": True,
        "undergraduate": True,
        "graduate": True,
        "active": True,
        "school_id": True,
        "created_at": False,
        "modified_at": False,
    }

    department_page = departments.paginate(page=page, per_page=10)

    only_fields = [k for k, v in dump_fields.items() if v]
    department_schema = DepartmentSchema(only=only_fields)

    res = fl.make_response(
        fl.jsonify(
            {
                "message": "success",
                "university_id": university_id,
                "page": page,
                "total_pages": department_page.pages,
                "total_results": departments.count(),
                "max_results_per_page": 10,
                "results": department_schema.dump(department_page, many=True),
            }
        )
    )

    res.mimetype = "application/json"

    return res, 200

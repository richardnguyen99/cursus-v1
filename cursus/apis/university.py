# -*- coding: utf-8 -*-

"""
University API endpoint handlers
"""

import flask

from cursus.models.university import (
    University,
    UniversityDomain,
    UniversityCampus,
    UniversityFounder,
)
from cursus.schema.university import (
    UniversitySchema,
    UniversityDomainSchema,
    UniversityCampusSchema,
    UniversityFounderSchema,
)


def _message_not_found(short_name: str):
    return f"\
University with short name `{short_name}` not found. If you want to add this \
university, please open a pull request at \
https://github.com/richardnguyen99/cursus/pulls."


def _domain_message_not_found(short_name: str):
    return f"\
University with short name `{short_name}` might not exist or have no domain. \
If you want to add this university or its domains, please open a pull request \
at https://github.com/richardnguyen99/cursus/pulls."


def _campus_message_not_found(short_name: str):
    return f"\
University with short name `{short_name}` might not exist or have no campus. \
If you want to add this university or its campuses, please open a pull \
request at https://github.com/richardnguyen99/cursus/pulls."


def _founder_message_not_found(short_name: str):
    return f"\
University with short name `{short_name}` might not exist or have no record \
of founders. If you want to add this university or its founders, please open \
a pull request at https://github.com/richardnguyen99/cursus/pulls."


def university_by_short_name(short_name: str):
    """Get a university by its short name (code)"""

    dump_fields = (
        "id",
        "full_name",
        "established",
        "former_name",
        "motto",
        "type",
        "created_at",
        "updated_at",
        "homepage",
    )

    university = University.query.filter_by(short_name=short_name).first()

    if university is None:
        response = flask.make_response(
            flask.jsonify(
                {
                    "message": _message_not_found(short_name),
                    "short_name": short_name.lower(),
                    "result": {},
                }
            )
        )
        response.mimetype = "application/json"

        return response, 404

    university_schema = UniversitySchema(only=dump_fields)

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "short_name": short_name.lower(),
                "result": university_schema.dump(university),
            }
        )
    )
    response.mimetype = "application/json"

    return response, 200


def university_domains_by_short_name(short_name: str):
    """Get a university's domains by its short name (code)"""

    req = flask.request

    page = req.args.get("page", 1, type=int)
    domain_type = req.args.get("type", None, type=str)
    locale = req.args.get("locale", None, type=str)

    dump_fields = (
        "id",
        "domain_name",
        "iso639_1",
        "type",
        "created_at",
        "updated_at",
    )

    domains = UniversityDomain.query.filter(
        UniversityDomain.school_short_name == short_name
    )

    if domains.count() == 0:
        response = flask.make_response(
            flask.jsonify(
                {
                    "message": _domain_message_not_found(short_name),
                    "short_name": short_name.lower(),
                    "result": {},
                }
            )
        )
        response.mimetype = "application/json"

        return response, 404

    if domain_type is not None:
        domain_type = domain_type.strip().lower()
        domains = domains.filter(UniversityDomain.type == domain_type)

    if locale is not None:
        locale = locale.strip().lower()
        domains = domains.filter(
            UniversityDomain.iso639_1.ilike(f"%{locale}%")
        )

    domain_schema = UniversityDomainSchema(only=dump_fields)
    domain_page = domains.paginate(page=page, per_page=10, error_out=False)

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "Success",
                "short_name": short_name.lower(),
                "page": page,
                "total_pages": domain_page.pages,
                "total_domains": domains.count(),
                "resullt": domain_schema.dump(domain_page.items, many=True),
            }
        )
    )
    response.mimetype = "application/json"

    return response, 200


def university_campuses_by_short_name(short_name: str):
    """Get a university's campuses by its short name (code)"""

    req = flask.request

    page = req.args.get("page", 1, type=int)

    dump_fields = (
        "address_id",
        "address_street",
        "address_city",
        "address_state",
        "address_zip_code",
        "country_code",
        "school_short_name",
        "created_at",
        "updated_at",
    )

    campuses = UniversityCampus.query.filter(
        UniversityCampus.school_short_name == short_name
    )

    if campuses.count() == 0:
        response = flask.make_response(
            flask.jsonify(
                {
                    "message": _campus_message_not_found(short_name),
                    "short_name": short_name.lower(),
                    "result": {},
                }
            )
        )
        response.mimetype = "application/json"

        return response, 404

    campus_schema = UniversityCampusSchema(only=dump_fields)

    campus_page = campuses.paginate(page=page, per_page=10, error_out=False)

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "success",
                "short_name": short_name.lower(),
                "page": page,
                "total_pages": campus_page.pages,
                "total_campuses": campuses.count(),
                "result": campus_schema.dump(campus_page.items, many=True),
            }
        )
    )
    response.mimetype = "application/json"

    return response, 200


def university_founders_by_short_name(short_name: str):
    """Get a university's campuses by its short name (code)"""

    req = flask.request

    page = req.args.get("page", 1, type=int)

    dump_fields = (
        "id",
        "biography_link",
        "first_name",
        "last_name",
        "middle_name",
        "suffix",
        "created_at",
        "updated_at",
    )

    founders = UniversityFounder.query.filter(
        UniversityFounder.school_short_name == short_name
    )

    if founders.count() == 0:
        response = flask.make_response(
            flask.jsonify(
                {
                    "message": _founder_message_not_found(short_name),
                    "short_name": short_name.lower(),
                    "result": {},
                }
            )
        )
        response.mimetype = "application/json"

        return response, 404

    founder_page = founders.paginate(page=page, per_page=10, error_out=False)
    founder_schema = UniversityFounderSchema(only=dump_fields)

    response = flask.make_response(
        flask.jsonify(
            {
                "message": "success",
                "page": page,
                "total_pages": founder_page.pages,
                "total_founders": founders.count(),
                "school_short_name": short_name.lower(),
                "result": founder_schema.dump(founder_page.items, many=True),
            }
        )
    )
    response.mimetype = "application/json"

    return response, 200

# -*- coding: utf-8 -*-

"""
Search enpoint handlers
"""

import flask
import sqlalchemy as sa

from cursus.schema import UniversitySchema
from cursus.models import University, UniversityCampus
from cursus.util.exceptions import (
    BadRequestError,
)


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

    if not query:
        raise BadRequestError(
            "Query string cannot be empty while using this endpoint"
        )

    if len(query) < 3:
        raise BadRequestError(
            "Query string must be at least 3 characters long"
        )

    search_string = f"%{query}%"

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

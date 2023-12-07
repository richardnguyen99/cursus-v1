import flask
import urllib.parse

from sqlalchemy.orm import joinedload

from cursus.util import CursusException
from cursus.models.university import University
from cursus.schema.university import (
    UniversitySchema,
)


def university_index():
    """University index endpoint"""

    raise CursusException.NotFoundError(
        "This URL, `/university/`, is unavailable"
    )


def university_find():
    """University find endpoint with query string"""

    # Get request query string
    query_string = flask.request.query_string.decode("utf-8")

    # Check if query string is empty
    if not query_string:
        reason = "Query string cannot be empty while using this endpoint"
        raise CursusException.BadRequestError(reason)

    # Parse query string into a dictionary of arguments
    query_dict = urllib.parse.parse_qs(query_string)

    # parse_qs returns a list of values for each key. This will convert the
    # list into a single value.
    parsed_dict = {key: value[0] for key, value in query_dict.items()}

    # Check if query string contains a `school` argument and has a value
    if "school" not in parsed_dict or not parsed_dict["school"]:
        reason = "Query string must contain a `school` argument"
        raise CursusException.BadRequestError(reason)

    # Set the default limit
    limit = 5

    if "limit" in parsed_dict and parsed_dict["limit"]:
        try:
            limit_from_query = int(parsed_dict["limit"])

            if limit_from_query > 0:
                limit = min(limit_from_query, 10)
            else:
                raise ValueError
        except ValueError:
            reason = "Query string `limit` argument must be a positive integer\
in the range [1, 10]"
            raise CursusException.BadRequestError(reason)

    search_string = parsed_dict["school"]

    # Search string with ignored-case pattern
    universities = University.query.filter(
        University.full_name.ilike(f"%{search_string}%")
    ).limit(limit)

    # Schema dump options
    fields = {
        "id": True,
        "full_name": True,
        "short_name": True,
    }

    only_fields = tuple([key for key, value in fields.items() if value])

    university_schema = UniversitySchema(only=only_fields)
    count = universities.count()

    resp = flask.make_response(
        flask.json.dumps(
            {
                "message": "OK" if count > 0 else "No results found",
                "data": university_schema.dump(
                    universities.all(),
                    many=True,
                ),
                "count": count,
            }
        ),
        200,
    )

    resp.headers["Content-Type"] = "application/json"

    return resp


def university_get_by_name(name: str):
    """University get by name endpoint"""

    if flask.request.method != "GET":
        uri = flask.request.url

        raise CursusException.MethodNotAllowedError(
            f"This endpoint, {uri}, only accepts GET requests"
        )

    university = University.query.filter(
        University.short_name.ilike(f"{name}")
    ).first()

    if not university:
        raise CursusException.BadRequestError(
            f"University with code name, {name}, not found"
        )

    # Schema dump options
    fields = {
        "id": True,
        "full_name": True,
        "short_name": True,
        "established": True,
        "former_name": True,
        "motto": True,
        "campuses": True,
        "domains": True,
        "founders": True,
        "updated_at": True,
        "created_at": True,
    }

    only_fields = tuple([key for key, value in fields.items() if value])

    university_schema = UniversitySchema(only=only_fields)

    resp = flask.make_response(
        flask.json.dumps(
            {
                "message": "OK",
                "data": university_schema.dump(
                    university,
                ),
            }
        ),
        200,
    )
    resp.headers["Content-Type"] = "application/json"

    return resp

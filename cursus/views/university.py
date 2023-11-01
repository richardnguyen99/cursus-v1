import flask
import urllib.parse

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from cursus.util import CursusException
from cursus.models.university import University
from cursus.schema.university import university_schema


def university_index():
    """University index endpoint"""

    raise CursusException.NotFoundError(
        "This URL, `/university/`, is unavailable"
    )


def university_find():
    """University find endpoint with query string"""

    if flask.request.method != "GET":
        raise CursusException.MethodNotAllowedError(
            "This endpoint only accepts GET requests"
        )

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

    # Check if query string contains a `s` argument and has a value
    if "s" not in parsed_dict or not parsed_dict["s"]:
        reason = "Query string must contain a `s` argument"
        raise CursusException.BadRequestError(reason)

    search_string = parsed_dict["s"]

    universities = University.query.filter(
        func.lower(University.full_name).like(f"%{search_string}%")
    )

    limit = 10

    # Check if query string contains a `limits` argument and has a value
    if "limit" in parsed_dict and parsed_dict["limit"]:
        try:
            limit = int(parsed_dict["limit"])
        except ValueError:
            reason = "Query string `limit` argument must be an integer"
            raise CursusException.BadRequestError(reason)

    universities = (
        universities.limit(limit).options(joinedload(University.domains)).all()
    )

    resp = flask.make_response(
        flask.json.dumps(
            {
                "message": "OK",
                "data": university_schema.dump(universities, many=True),
            }
        ),
        200,
    )

    resp.headers["Content-Type"] = "application/json"
    return resp


def university_get_by_name(name: str):
    """University get by name endpoint"""

    resp = flask.make_response(
        flask.json.dumps(
            {
                "message": "OK",
                "data": {
                    "name": name,
                },
            }
        ),
        200,
    )
    resp.headers["Content-Type"] = "application/json"

    return resp

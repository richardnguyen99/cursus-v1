import flask

from cursus.util import CursusException


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

    else:
        # Split query string into a list of arguments
        # TODO:

        resp = flask.make_response(
            flask.json.dumps(
                {
                    "message": "OK",
                    "data": {
                        "query_string": query_string,
                    },
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

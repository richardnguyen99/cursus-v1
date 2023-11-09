import flask


def find_index():
    """Find index endpoint"""

    resp = flask.make_response(
        flask.json.dumps({"message": "This URL is unavailable"}), 400
    )
    resp.headers["Content-Type"] = "application/json"

    return resp


def find_university(university_name: str):
    """Find a university by its ID."""
    resp = flask.make_response(
        flask.json.dumps(
            {
                "message": "OK",
                "data": {
                    "university_name": university_name,
                },
            }
        ),
        200,
    )
    resp.headers["Content-Type"] = "application/json"

    return resp

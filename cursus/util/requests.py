# -*- coding: utf-8 -*-

"""
Utility function for handling and processing requests
"""

import urllib

from typing import Optional, Dict

from . import exceptions as CursusException


def get_parsed_dict(query_string: str) -> Optional[Dict]:
    """Prepare a parsed dicctionary from the given query string"""

    # Check if query string is empty
    if not query_string:
        return None

    # Parse query string into a dictionary of arguments
    query_dict = urllib.parse.parse_qs(query_string)

    # parse_qs returns a list of values for each key. This will convert the
    # list into a single value.
    parsed_dict = {key: value[0] for key, value in query_dict.items()}

    return parsed_dict


def has_require_params(parsed_dict: dict, required_params: list[str]) -> bool:
    """Get the required parameters from the parsed dictionary"""

    # Check if query string contains a `school` argument and has a value
    for param in required_params:
        if param not in parsed_dict or not parsed_dict[param]:
            return False

    return True


def get_limit(
    parsed_dict: dict,
    default_value: Optional[int] = 5,
    min_value: Optional[int] = 0,
    max_value: Optional[int] = 10,
) -> int:
    """Get the limit from the parsed dictionary to be used in a query

    It guarantees to work if the following conditions are met:
    - `parsed_dict` is not None and is a dictionary, `dict`
    - `default_value`, `min_value`, and `max_value` are integers, `int`
    - `min_value` is less than or equal to `max_value`.
    - `default_value` must be between `min_value` and `max_value`.

    Otherwise, it will raise an Exception with a message that describes the
    error.
    """

    if not isinstance(parsed_dict, dict):
        raise Exception("Parsed dictionary must be a dictionary")

    DEFAULT_VALUE = default_value or 5
    MIN_VALUE = min_value or 0
    MAX_VALUE = max_value or 10

    if "limit" not in parsed_dict or not parsed_dict["limit"]:
        return DEFAULT_VALUE

    limit = DEFAULT_VALUE

    try:
        limit = int(parsed_dict["limit"])
    except ValueError:
        limit = DEFAULT_VALUE

    if limit < MIN_VALUE:
        limit = MIN_VALUE
    elif limit > MAX_VALUE:
        limit = MAX_VALUE

    return limit

"""
String Builder class for building strings dynamically.
"""

import io


class StringBuilder:
    _str_io: io.StringIO

    def __init__(self):
        self._str_io = io.StringIO()

    def __str__(self):
        return ""

    def append(self, value: str) -> None:
        self._str_io.write(value)

    def build(self) -> str:
        return self._str_io.getvalue()

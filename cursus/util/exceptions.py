# -*- coding: utf-8 -*-

"""List of custom exceptions used by the Cursus application
"""

__all__ = [
    "CursusError",
    "BadRequestError",
    "NotFoundError",
    "MethodNotAllowedError",
    "InternalServerError",
]


class CursusError(Exception):
    """Base class for Cursus exceptions"""

    status_code: int
    status_msg: str
    reason: str

    def __init__(self, status_code: int, status_msg: str, reason: str):
        self.status_code = status_code
        self.status_msg = status_msg
        self.reason = reason

    def __str__(self):
        return f"{self.status_code} {self.status_msg}: {self.reason}"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.status_code}>"

    def get_reason(self):
        return self.reason


class BadRequestError(CursusError):
    """Exception raised when a bad request is made"""

    def __init__(self, reason: str):
        super().__init__(400, "Bad Request", reason)


class UnauthorizedError(CursusError):
    """Exception raised when an unauthorized request is made"""

    def __init__(self, reason: str):
        super().__init__(401, "Unauthorized", reason)


class ForbiddenError(CursusError):
    """Exception raised when a forbidden request is made"""

    def __init__(self, reason: str):
        super().__init__(403, "Forbidden", reason)


class NotFoundError(CursusError):
    """Exception raised when a request to a non-existent resource is made"""

    def __init__(self, reason: str):
        super().__init__(404, "Not Found", reason)


class MethodNotAllowedError(CursusError):
    """Exception raised when a request to a resource is made with an
    unsupported method
    """

    def __init__(self, reason: str):
        super().__init__(405, "Method Not Allowed", reason)


class InternalServerError(CursusError):
    """Exception raised when an internal server error occurs"""

    def __init__(self, reason: str):
        super().__init__(500, "Internal Server Error", reason)

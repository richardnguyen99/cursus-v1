# -*- coding: utf-8 -*-

"""Module util that provides utility functions and objects for the application
"""

from .extensions import db  # noqa: F401
from . import exceptions as CursusException  # noqa: F401
from .generate_content_hash import generate_content_hash  # noqa: F401

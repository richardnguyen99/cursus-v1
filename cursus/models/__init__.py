# -*- coding: utf-8 -*-

"""Cursus models module
"""

from .country import Country
from .token import ActiveToken
from .user import User, Account, Session, VerificationToken
from .history import History
from .course import Course
from .department import Department
from .school import School
from .university import (
    University,
    UniversityCampus,
    UniversityDomain,
    UniversityFounder,
)

# -*- coding: utf-8 -*-

"""
Schema Module for Cursus Application
"""

from .country import CountrySchema
from .school import SchoolSchema
from .department import DepartmentSchema
from .university import (
    UniversitySchema,
    UniversityCampusSchema,
    UniversityDomainSchema,
    UniversityFounderSchema,
)

# -*- coding: utf-8 -*-

"""
Schema Module for Cursus Application
"""

from .country import CountrySchema
from .school import SchoolSchema
from .university import (
    UniversitySchema,
    UniversityCampusSchema,
    UniversityDomainSchema,
    UniversityFounderSchema,
)

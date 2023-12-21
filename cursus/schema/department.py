# -*- coding: utf-8 -*-

"""
Department-related Schema
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from cursus.models import Department


class DepartmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    code = auto_field()
    university_id = auto_field()
    school_id = auto_field()
    website = auto_field()
    undergraduate = auto_field()
    graduate = auto_field()
    active = auto_field()
    type = auto_field()
    special_name = auto_field()
    created_at = auto_field(dump_only=True)
    modified_at = auto_field(dump_only=True)

    university_name = fields.String(dump_only=True)
    school_name = fields.String(dump_only=True)

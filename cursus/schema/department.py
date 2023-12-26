# -*- coding: utf-8 -*-

"""
Department-related Schema
"""

from typing import Any
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

    full_name = fields.Method("get_full_name")
    university_name = fields.String(dump_only=True)
    school_name = fields.String(dump_only=True)

    def get_full_name(self, obj: Department) -> str:
        special_name = (
            f"{obj.special_name} " if obj.special_name != "-" else ""
        )
        department_type = obj.type.capitalize()

        return f"{special_name}{department_type} of {obj.name}"

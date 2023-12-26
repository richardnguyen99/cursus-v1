# -*- coding: utf-8 -*-

"""
School-related Schema
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from cursus.models import School
from cursus.schema.department import DepartmentSchema


class SchoolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = School
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    website = auto_field()
    created_at = auto_field()
    modified_at = auto_field()
    university_id = auto_field()

    university_full_name = fields.String(dump_only=True)
    university_short_name = fields.String(dump_only=True)

    departments = fields.Nested(
        DepartmentSchema,
        only=(
            "id",
            "name",
            "code",
        ),
        many=True,
    )

    total_departments = fields.Integer(dump_only=True)

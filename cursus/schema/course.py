# -*- coding: utf-8 -*-

"""
Course-related Schema
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from cursus.models import Course


class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        include_relationships = True

    id = auto_field()
    title = auto_field()
    code = auto_field()
    department_id = auto_field()
    university_id = auto_field()
    website = auto_field()
    description = auto_field()
    active = auto_field()
    description = auto_field()
    credits = auto_field()
    created_at = auto_field(dump_only=True)
    modified_at = auto_field(dump_only=True)

    level = fields.Method("get_level", dump_only=True)
    department_name = fields.String()
    university_name = fields.String()

    def get_level(self, obj: Course):
        if obj.level == 1:
            return "undergraduate"

        if obj.level == 2:
            return "graduate"

        if obj.level == 3:
            return "doctorate"

        return "unknown"

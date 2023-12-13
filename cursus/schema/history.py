# -*- coding: utf-8 -*-

"""
History-related schema
"""


from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from cursus.models.history import History


class HistorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = History
        load_instance = True
        include_fk = True

    id = auto_field()
    user_id = auto_field()
    token_used = auto_field()
    type = auto_field()
    at = fields.DateTime("%Y-%m-%d %H:%M:%S")

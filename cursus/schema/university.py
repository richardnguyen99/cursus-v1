# -*- coding: utf-8 -*-

"""
University-related Schema
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from cursus.models.university import (
    University,
    UniversityDomain,
    UniversityFounder,
    UniversityCampus,
)
from cursus.schema.country import CountrySchema


class UniversityDomainSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UniversityDomain
        load_instance = True
        include_fk = True

    id = auto_field()
    domain_name = auto_field()


class UniversityFounderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UniversityFounder
        load_instance = True
        include_fk = True

    id = auto_field()
    founder_name = auto_field()
    biography_link = auto_field()


class UniversityCampusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UniversityCampus
        load_instance = True
        include_fk = True

    address_id = auto_field()
    address_number = auto_field()
    address_street = auto_field()
    address_city = auto_field()
    address_state = auto_field()
    address_zip_code = auto_field()
    country_code = auto_field()

    country = fields.Nested(CountrySchema, only=("name",), many=False)

    address = fields.Method("get_address", dump_only=True)

    def get_address(self, obj: UniversityCampus):
        return f"{obj.address_number}, \
{obj.address_street} \
{obj.address_city}, \
{obj.address_state}, \
{obj.address_zip_code}, \
{obj.country.name}"


class UniversitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = University
        load_instance = True
        include_relationships = True

    id = auto_field()
    full_name = auto_field(dump_only=True)
    short_name = auto_field(dump_only=True)
    established = auto_field(dump_only=True)
    former_name = auto_field(dump_only=True)
    motto = auto_field()

    domains = fields.Nested(
        UniversityDomainSchema, many=True, only=("domain_name",)
    )

    founders = fields.Nested(
        UniversityFounderSchema, many=True, only=("founder_name",)
    )

    campuses = fields.Method(
        "get_campuses",
        dump_only=True,
    )

    def get_campuses(self, obj: University):
        return [
            "{0}, {1}, {2}, {3} {4}".format(
                campus.address_number,
                campus.address_street,
                campus.address_city,
                campus.address_state,
                campus.address_zip_code,
            )
            for campus in obj.campuses
        ]


university_schema = UniversitySchema()
university_domain_schema = UniversityDomainSchema()

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
from cursus.util.string_builder import StringBuilder


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
    first_name = auto_field()
    last_name = auto_field()
    middle_name = auto_field()
    suffix = auto_field()
    biography_link = auto_field()

    @staticmethod
    def build(founder: UniversityFounder):
        string_builder = StringBuilder()

        string_builder.append(founder.first_name)
        string_builder.append(" ")

        if founder.middle_name and founder.middle_name != "-":
            string_builder.append(founder.middle_name)
            string_builder.append(" ")

        string_builder.append(founder.last_name)

        if founder.suffix and founder.suffix != "-":
            string_builder.append(", ")
            string_builder.append(founder.suffix)

        return string_builder.build()


class UniversityCampusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UniversityCampus
        load_instance = True
        include_fk = True

    address_id = auto_field()
    address_street = auto_field()
    address_city = auto_field()
    address_state = auto_field()
    address_zip_code = auto_field()
    # country_code = auto_field()

    country = fields.Nested(
        CountrySchema,
        only=(
            "name",
            "alpha3",
            "iso3166_2",
            "region",
            "subregion",
        ),
        many=False,
    )

    address = fields.Method("get_address", dump_only=True)

    def get_address(self, obj: UniversityCampus):
        return f"{obj.address_street}, \
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

    campuses = fields.Nested(
        lambda: UniversityCampusSchema(
            only=(
                "address_street",
                "address_city",
                "address_state",
                "address_zip_code",
                "country_code",
                "country",
            )
        ),
        many=True,
        dump_only=True,
    )

    domains = fields.Nested(
        UniversityDomainSchema,
        many=True,
        only=("domain_name", "iso639_1", "type"),
        dump_only=True,
    )

    founders = fields.Nested(
        UniversityFounderSchema,
        many=True,
        dump_only=True,
        only=(
            "last_name",
            "first_name",
            "middle_name",
            "suffix",
            "biography_link",
        ),
    )

    def get_campuses(self, obj: University):
        return [
            "{0}, {1}, {2}, {3}".format(
                campus.address_street,
                campus.address_city,
                campus.address_state,
                campus.address_zip_code,
            )
            for campus in obj.campuses
        ]

    def get_founder_strs(self, obj: University):
        return [
            UniversityFounderSchema.build(founder) for founder in obj.founders
        ]

    def get_domains(self, obj: University):
        return [domain.domain_name for domain in obj.domains]


university_schema = UniversitySchema()
university_domain_schema = UniversityDomainSchema()

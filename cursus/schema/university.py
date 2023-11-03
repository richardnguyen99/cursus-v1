from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields

from cursus.util.extensions import ma
from cursus.models.university import (
    University,
    UniversityDomain,
    UniversityFounder,
    UniversityCampus,
)


class UniversityDomainSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UniversityDomain
        load_instance = True
        include_fk = True

    id = auto_field()
    domain_name = auto_field()
    school_id = auto_field()


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


class UniversitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = University
        load_instance = True
        include_relationships = True

    id = auto_field()
    full_name = auto_field()
    state = auto_field()
    country = auto_field()

    domains = fields.Nested(
        UniversityDomainSchema, many=True, only=("domain_name",)
    )

    founders = fields.Nested(
        UniversityFounderSchema, many=True, only=("founder_name",)
    )

    campuses = fields.Nested(
        UniversityCampusSchema,
        many=True,
        only=(
            "address_number",
            "address_street",
            "address_city",
            "address_state",
            "address_zip_code",
            "country_code",
        ),
    )


university_schema = UniversitySchema()
university_domain_schema = UniversityDomainSchema()

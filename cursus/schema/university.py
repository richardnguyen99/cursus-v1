from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields

from cursus.util.extensions import ma
from cursus.models.university import University, UniversityDomain


class UniversityDomainSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UniversityDomain
        load_instance = True
        include_fk = True

    id = auto_field()
    domain_name = auto_field()
    school_id = auto_field()


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


university_schema = UniversitySchema()
university_domain_schema = UniversityDomainSchema()

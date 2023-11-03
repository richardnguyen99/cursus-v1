import marshmallow
import marshmallow_sqlalchemy as masqla

from cursus.models.country import Country


class CountrySchema(masqla.SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        load_instance = True

    id = marshmallow.fields.Integer(dump_only=True)
    name = marshmallow.fields.String(required=True)
    alpha2 = marshmallow.fields.String(required=True)
    alpha3 = marshmallow.fields.String(required=True)
    country_code = marshmallow.fields.String(required=True)
    iso3166_2 = marshmallow.fields.String(required=True)
    region = marshmallow.fields.String(required=True)
    subregion = marshmallow.fields.String(required=True)
    region_code = marshmallow.fields.String(required=True)
    sub_region_code = marshmallow.fields.String(required=True)

    created_at = marshmallow.fields.DateTime(dump_only=True)
    updated_at = marshmallow.fields.DateTime(dump_only=True)

    name_alpha2 = marshmallow.fields.Method("get_name_alpha2", dump_only=True)

    def __repr__(self):
        return f"<CountrySchema (name={self.name})>"

    def get_name_alpha2(self, obj: Country):
        return f"{obj.name} ({obj.alpha2})"

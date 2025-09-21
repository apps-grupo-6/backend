from marshmallow import Schema, fields, validate

from configs import LocationsConfig

class create_location(Schema):
    owner_id = fields.Integer(required=True, validate=validate.Range(min=1))
    country_code = fields.String(required=True, validate=validate.OneOf(LocationsConfig.country_codes)) # ISO 3166-1 with A-2
    city = fields.String(required=True, validate=validate.Length(min=1, max=50))
    address = fields.String(required=True, validate=validate.Length(min=1, max=50))
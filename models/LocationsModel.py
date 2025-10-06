from marshmallow import Schema, fields, validate

from configs import LocationsConfig

class create_location(Schema):
    country_code = fields.String(required=True, validate=validate.OneOf(LocationsConfig.country_codes)) # ISO 3166-1 with A-2
    city = fields.String(required=True, validate=validate.Length(min=1, max=50))
    address = fields.String(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    lat = fields.Float(required=True, validate=validate.Range(min=-90.0, max=90.0))
    lng = fields.Float(required=True, validate=validate.Range(min=-180.0, max=180.0))
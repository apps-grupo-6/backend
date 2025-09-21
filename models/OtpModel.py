from marshmallow import Schema, fields, validate

class create_otp(Schema):
    type = fields.String(required=True, validate=validate.Length(min=1, max=7))

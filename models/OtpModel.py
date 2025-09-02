from marshmallow import Schema, fields, validate

class create_otp(Schema):
    user_id = fields.String(required=True, validate=validate.Length(min=1, max=50))

    class Meta:
        unknown = 'exclude'
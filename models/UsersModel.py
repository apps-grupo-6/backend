from marshmallow import Schema, fields, validate

class register_account(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    password = fields.String(required=True, validate=validate.Length(min=1, max=50))
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    telephone = fields.String(required=True, validate=validate.Length(min=1, max=14))
    contact_email = fields.String(required=True, validate=validate.Length(min=1, max=100))

    class Meta:
        unknown = 'exclude'
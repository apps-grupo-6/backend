from marshmallow import Schema, fields, validate

class login(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    password = fields.String(required=True, validate=validate.Length(min=1, max=50))

    class Meta:
        unknown = 'exclude'

class login_otp(Schema):
    otp_token = fields.String(required=True, validate=validate.Length(min=1, max=6))

    class Meta:
        unknown = 'exclude'
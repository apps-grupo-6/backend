from marshmallow import Schema, fields, validate

class register_account(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    password = fields.String(required=True, validate=validate.Length(min=1, max=50))
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    telephone = fields.String(required=True, validate=validate.Length(min=1, max=14))
    contact_email = fields.String(required=True, validate=validate.Length(min=1, max=100))

class update_user_information(Schema):
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    telephone = fields.String(required=False)
    contact_email = fields.String(required=False)

class resend_otp(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    type = fields.String(required=True, validate=validate.OneOf(['REGISTRATION', 'RECOVERY']))

class reset_password(Schema):
    reset_token = fields.String(required=True, validate=validate.Length(min=1))
    new_password = fields.String(required=True, validate=validate.Length(min=6, max=100))

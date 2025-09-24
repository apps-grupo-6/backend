from marshmallow import Schema, fields, validate

class login(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    password = fields.String(required=True, validate=validate.Length(min=1, max=50))

class login_otp(Schema):
    otp_token = fields.String(required=True, validate=validate.Length(min=1, max=6))

class refresh_token(Schema):
    jwt_token = fields.String(required=True, validate=validate.Length(min=1))

class recover_account(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    new_password = fields.String(required=True, validate=validate.Length(min=1, max=50))
    otp_token = fields.String(required=True, validate=validate.Length(min=1, max=6))

class verify_otp(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    verification_code = fields.String(required=True, validate=validate.Length(min=1, max=6))

class resend_otp(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    type = fields.String(required=True, validate=validate.OneOf(['REGISTRATION', 'RECOVERY']))

class reset_password(Schema):
    reset_token = fields.String(required=True, validate=validate.Length(min=1))
    new_password = fields.String(required=True, validate=validate.Length(min=6, max=100))


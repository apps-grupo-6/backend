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

class confirm_account(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    otp_token = fields.String(required=True, validate=validate.Length(min=1, max=6))


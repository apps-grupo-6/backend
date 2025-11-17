from marshmallow import Schema, fields, validate

class login(Schema):
    username = fields.String(required=True, validate=validate.Length(min=6, max=12))
    password = fields.String(required=True, validate=validate.Length(min=1, max=50))

class refresh_token(Schema):
    jwt_token = fields.String(required=True, validate=validate.Length(min=1))

class recover_account(Schema):
    username = fields.String(required=True, validate=validate.Length(min=6, max=12))
    new_password = fields.String(required=False, allow_none=True, validate=validate.Length(min=1, max=50))

class confirm_account(Schema):
    username = fields.String(required=True, validate=validate.Length(min=6, max=12))


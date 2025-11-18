from marshmallow import Schema, fields, validate

class set_user_token(Schema):
    expo_push_token = fields.String(required=True, validate=validate.Length(min=1, max=255))

from marshmallow import Schema, fields, validate

from configs import OtpConfig

class create_otp(Schema):
    type = fields.String(required=True, validate=validate.OneOf(["LOGIN", "RECOVER"]))

class resend_otp(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    type = fields.String(required=True, validate=validate.OneOf(OtpConfig.OTP_TYPES))
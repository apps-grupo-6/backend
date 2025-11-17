from marshmallow import Schema, fields, validate
from configs import NotificationsConfig

class set_user_token(Schema):
    expo_push_token = fields.String(required=True, validate=validate.OneOf(NotificationsConfig.NOTIFICATION_TYPES))

class create_notification(Schema):
    type = fields.String(required=True, validate=validate.Length(min=1, max=10))
    class_id = fields.Int(required=True)

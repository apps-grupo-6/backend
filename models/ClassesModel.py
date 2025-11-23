from marshmallow import Schema, fields, validate

class create_class(Schema):
    professor_id = fields.String(required=False, allow_none=True, validate=validate.Length(min=1, max=50))
    location_id = fields.String(required=True, validate=validate.Length(min=1, max=50))
    discipline_id = fields.String(required=True, validate=validate.Length(min=1, max=50))
    scheduled_at = fields.String(required=True, validate=validate.Length(min=1, max=50))
    max_participants = fields.Integer(required=True, validate=validate.Range(min=1, max=50))
    qr = fields.String(required=True, validate=validate.Length(min=1, max=150))

class update_class(Schema):
    location_id = fields.String(required=False, allow_none=True, validate=validate.Length(min=1, max=50))
    discipline_id = fields.String(required=False, allow_none=True, validate=validate.Length(min=1, max=50))
    scheduled_at = fields.String(required=False, allow_none=True, validate=validate.Length(min=1, max=50))
    max_participants = fields.String(required=False, allow_none=True, validate=validate.Range(min=1, max=50))
    qr = fields.String(required=False, allow_none=True, validate=validate.Length(min=1, max=150))
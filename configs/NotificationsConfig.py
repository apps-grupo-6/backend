NOTIFICATION_TYPES = ("CANCELLED_CLASS", "RESCHEDULED_CLASS")

create_notification_code_map = {
    "0200": ("ok", 200),
    "0201": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid class_id", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}

set_user_token_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0500": ("the request could not be processed", 500)
}

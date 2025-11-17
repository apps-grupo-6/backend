OTP_TYPES = ("RECOVER", "REGISTRATION")

create_otp_code_map = {
    "0200": ("ok", 200),
    "0204": ("invalid user_id", 204),
    "0400": ("bad request", 400),
    "0410": ("the user already has an active otp_token with this type", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

resend_otp_code_map = {
    "0200": ("ok", 200),
    "0201": ("new otp_token was generated and sent", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid username", 404),
    "0410": ("the username does not have any otp_token active with this type", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

check_otp_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid username", 404),
    "0405": ("invalid otp_token", 404),
    "0410": ("the username does not have any otp_token active with this type", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}

delete_otp_code_map = {
    "0200": ("ok", 200),
    "0404": ("invalid otp_token id", 400),
    "0500": ("the request could not be processed", 500)
}
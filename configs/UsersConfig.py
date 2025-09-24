register_account_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0410": ("username already exists", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}

verify_registration_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid username or verification code", 404),
    "0410": ("verification code expired", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}

get_user_information_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0410": ("all updatable fields are empty", 400),
    "0500": ("the request could not be processed", 500)
}

update_user_information_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0410": ("all updatable fields are empty", 400),
    "0500": ("the request could not be processed", 500)
}

resend_otp_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("username not found", 404),
    "0411": ("account already verified or invalid request", 400),
    "0412": ("account not verified, cannot request recovery", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

reset_password_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0413": ("invalid reset token", 401),
    "0414": ("reset token expired", 401),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}

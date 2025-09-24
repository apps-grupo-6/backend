from configs.ServerConfig import config

if config.get('Auth', 'enabled') == "1":
    jwt_secret = config.get('Auth', 'jwt_secret')
    jwt_algorithm = config.get('Auth', 'jwt_algorithm')
    jwt_exp_delta_seconds = int(config.get('Auth', 'jwt_exp_delta_seconds'))

login_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid username", 404),
    "0410": ("username or password are incorrect", 400),
    "0412": ("user's account is not verified", 400),
    "0500": ("the request could not be processed", 500)
}

login_otp_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid otp_token", 404),
    "0410": ("otp_token expired", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

refresh_token_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0410": ("requested jwt token is valid and did not expire yet", 400),
    "0411": ("requested jwt token is invalid", 400),
    "0500": ("the request could not be processed", 500),
}

verify_otp_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid verification code", 404),
    "0410": ("verification code expired", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
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

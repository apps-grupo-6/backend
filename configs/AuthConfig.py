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
    "0500": ("the request could not be processed", 500)
}

login_otp_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid username or otp_token", 404),
    "0411": ("otp_token expired", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}
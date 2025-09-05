from configs.ServerConfig import config

if config.get('Auth', 'enabled') == "1":
    jwt_secret = config.get('Auth', 'jwt_secret')
    jwt_algorithm = config.get('Auth', 'jwt_algorithm')
    jwt_exp_delta_seconds = int(config.get('Auth', 'jwt_exp_delta_seconds'))

login_code_map = {
    "0200": "ok",
    "0204": "invalid username",
    "0400": "bad request",
    "0410": "username or password are incorrect",
    "0500": "the request could not be processed"
}

login_otp_code_map = {
    "0200": "ok",
    "0400": "bad request",
    "0410": "invalid username or otp_token",
    "0411": "otp_token expired",
    "0500": "the request could not be processed",
    "0501": "the request could not be processed"
}
from configs.ServerConfig import config

if config.get('auth', 'enabled') == "1":
    jwt_secret = config.get('auth', 'jwt_secret')
    jwt_algorithm = config.get('auth', 'jwt_algorithm')
    jwt_exp_delta_seconds = int(config.get('auth', 'jwt_exp_delta_seconds'))

login_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid username", 404),
    "0410": ("username or password are incorrect", 400),
    "0411": ("user's account is not verified", 400),
    "0412": ("user's account is banned", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}

refresh_token_code_map = {
    "0200": ("ok", 200),
    "0201": ("jwt did not expire yet", 200),
    "0410": ("requested jwt token is invalid", 400),
    "0500": ("the request could not be processed", 500)
}

recover_account_code_map = {
    "0200": ("ok", 200),
    "0201": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid username", 404),
    "0410": ("user's account is banned", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}

confirm_account_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid username", 404),
    "0410": ("the user's account is already verified", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

logout_code_map = {
    "0200": ("ok", 200)
}
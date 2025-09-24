import datetime, jwt

from flask import g
from configs.ServerConfig import logger

from utils import UsersUtils, AuthUtils, OtpUtils
from configs import AuthConfig
from repositories import AuthRepository, UsersRepository

def login(model, request_id):
    username = model["username"]
    password = model["password"]

    logger.info(f"{request_id} - '{username}' is trying to login")
    get_user_info = AuthRepository.get_username_info(username=username,
                                                     request_id=request_id,
                                                     errors_code_map={
                                                         "database_error_code": "0500",
                                                         "invalid_data_error_code": "0404"
                                                     })
    if get_user_info["error"]:
        return {}

    if not get_user_info['data']['email_verified']:
        logger.error(f"{request_id} - user's account is not verified")
        g.response_code = "0412"
        return {}

    user_id = get_user_info['data']['user_id']
    g.user_id = user_id

    logger.info(f"{request_id} - checking password...")
    if not UsersUtils.verify_password(plain_password=password, hashed_password=get_user_info["data"]["password"]):
        logger.error(f"{request_id} - the password is incorrect")
        g.response_code = "0410"
        return {}

    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds),
        "user_id": user_id
    }

    logger.info(f"{request_id} - generating jwt token...")
    token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)

    logger.info(f"{request_id} - first step login was done successfully")
    g.response_code = "0200"
    return {
        "data": {
            "token": token
        }
    }

def login_otp(model, user_id, request_id):
    otp_token = model["otp_token"]
    TYPE = "LOGIN"

    get_user_token = AuthRepository.check_otp_token(user_id=user_id,
                                                    otp_token=otp_token,
                                                    type=TYPE,
                                                    request_id=request_id,
                                                    errors_code_map={
                                                        "database_error_code": "0500",
                                                        "invalid_data_error_code": "0404"
                                                    })
    if get_user_token["error"]:
        return {}

    logger.info(f"{request_id} - checking if otp token is valid...")
    if OtpUtils.check_token_expired(checked=get_user_token):
        logger.error(f"{request_id} - user's login otp_token is expired")
        g.response_code = "0410"
        return {}

    deleted = OtpUtils.delete_otp_token(user_id=user_id,
                                        otp_token=otp_token,
                                        type=TYPE,
                                        request_id=request_id,
                                        errors_code_map={"database_error_code": "0501"})

    if not deleted:
        return {}

    last_login = AuthRepository.update_user_last_login(user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map={"database_error_code": "0502"})

    if last_login["error"]:
        return {}

    logger.info(f"{request_id} - second login step finished successfully; user has been authenticated")
    g.response_code = "0200"
    return {}

def refresh_token(model, request_id):
    jwt_token = model["jwt_token"]

    logger.info(f"{request_id} - checking if needed to refresh jwt token...")
    decoded = AuthUtils.check_jwt_token(jwt_token)

    if decoded["error"]:
        if decoded["error_code"] == 0:
            logger.error(f"{request_id} - the requested jwt token is valid and did not expire yet")
            g.response_code = "0410"
        else:
            logger.error(f"{request_id} - the requested jwt token is invalid")
            g.response_code = "0411"

        return {}
    else:
        logger.debug(f"{g.request_id} - jwt token is expired (ok)")

    decoded["data"]["exp"] += AuthConfig.jwt_exp_delta_seconds
    refreshed = jwt.encode(decoded, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)

    last_login = AuthRepository.update_user_last_login(user_id=decoded["data"]["user_id"],
                                                       request_id=request_id,
                                                       errors_code_map={"database_error_code": "0500"})

    if last_login["error"]:
        return {}

    g.response_code = "0200"
    return {
        "data": {
            "token": refreshed
        }
    }

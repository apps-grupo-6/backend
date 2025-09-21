import datetime, jwt
from random import shuffle

from flask import g
from configs.ServerConfig import logger

from utils import UsersUtils, AuthUtils, OtpUtils
from configs import AuthConfig
from repositories import AuthRepository, OtpRepository, UsersRepository


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

    user_id = get_user_info['data']['user_id']
    g.user_id = user_id

    logger.info(f"{request_id} - checking password...")
    if not UsersUtils.verify_password(plain_password=password, hashed_password=get_user_info["data"]["password"]):
        logger.critical(f"{request_id} - the password is incorrect")
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
        logger.info(f"{request_id} - user's login otp_token is expired")
        g.response_code = "0410"
        return {}

    deleted = OtpUtils.delete_otp_token(user_id=user_id,
                                        otp_token=otp_token,
                                        type=TYPE,
                                        request_id=request_id,
                                        errors_code_map={"database_error_code": "0501"})

    if not deleted:
        return {}

    logger.info(f"{request_id} - second login step finished successfully; user has been authenticated")
    g.response_code = "0200"
    return {}

def refresh_token(model, request_id):
    jwt_token = model["jwt_token"]

    logger.info(f"{request_id} - refreshing jwt token...")
    decoded = AuthUtils.check_jwt_token(jwt_token)
    if decoded["error"]:
        return decoded["error"], 401

    decoded["data"]["exp"] += AuthConfig.jwt_exp_delta_seconds
    refreshed = jwt.encode(decoded, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)

    logger.debug(f"{request_id} - jwt token refreshed successfully...")
    g.response_code = "0200"
    return {
        "data": {
            "token": refreshed
        }
    }

def recover_account(model, request_id):
    username = model["username"]
    new_password = model["new_password"]
    otp_token = model["otp_token"]
    TYPE = "RECOVER"

    exists_username = UsersRepository.check_if_username_exists(username=username,
                                                               request_id=request_id,
                                                               errors_code_map={
                                                                   "database_error_code": "0500",
                                                                   "invalid_data_error_code": "0404"
                                                               })

    if exists_username["error"]:
        return {}

    user_id = exists_username["data"]["id"]
    checked = AuthRepository.check_otp_token(user_id=user_id,
                                             otp_token=otp_token,
                                             type=TYPE,
                                             request_id=request_id,
                                             errors_code_map={
                                                 "database_error_code": "0501",
                                                 "invalid_data_error_code": "0405"
                                             })

    if checked["error"]:
        return {}

    if OtpUtils.check_token_expired(checked=checked):
        logger.info(f"{request_id} - user's recovery otp_token is expired")
        g.response_code = "0410"
        return {}

    hashed_password = UsersUtils.hash_password(plain_password=new_password)
    updated = AuthRepository.set_new_password(user_id=user_id,
                                              new_password=hashed_password,
                                              request_id=request_id)

    if not updated:
        logger.critical(f"{request_id} - an error occurred while updating user's password")
        g.response = "0502"
        return {}

    deleted = OtpUtils.delete_otp_token(user_id=user_id,
                                        otp_token=otp_token,
                                        type=TYPE,
                                        request_id=request_id,
                                        errors_code_map={"database_error_code": "0503"})

    if not deleted:
        return {}

    g.response_code = "0200"
    return {}
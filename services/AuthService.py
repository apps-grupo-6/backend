import datetime, jwt
from flask import g
from configs.ServerConfig import logger

from utils import UsersUtils
from configs import AuthConfig
from repositories import AuthRepository, OtpRepository

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

    get_user_token = AuthRepository.check_otp_token(user_id=user_id,
                                                    otp_token=otp_token,
                                                    request_id=request_id,
                                                    errors_code_map={
                                                        "database_error_code": "0500",
                                                        "invalid_data_error_code": "0404"
                                                    })
    if get_user_token["error"]:
        return {}

    logger.info(f"{request_id} - checking if otp token is valid...")
    if get_user_token["data"]["expires_at"] < datetime.datetime.now():
        logger.info(f"{request_id} - user's otp_token is expired")
        g.response_code = "0411"
        return {}

    deleted = OtpRepository.delete_otp(user_id=user_id,
                                       otp_token=otp_token,
                                       request_id=request_id,
                                       errors_code_map={"database_error_code": "0501"})

    if deleted["error"]:
        return {}

    logger.info(f"{request_id} - second login step finished successfully; user has been authenticated")
    g.response_code = "0200"
    return {}
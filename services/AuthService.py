import datetime, jwt
from flask import g
from configs.ServerConfig import logger

from utils import UsersUtils
from managers import AuthManager, OtpManager
from configs import AuthConfig

def login(model, request_id):
    username = model["username"]
    password = model["password"]

    logger.info(f"{request_id} - '{username}' is trying to login")
    get_user_info = AuthManager.login(username=username,
                                      request_id=request_id)

    if not get_user_info["ok"]:
        g.response_code = "0500"
        logger.critical(f"{request_id} - database failed when this user tried to login")
        return {"code": "0500", "description": AuthConfig.login_code_map["0500"]}, 500

    if not get_user_info["data"]:
        g.response_code = "0204"
        logger.critical(f"{request_id} - invalid username")
        return {"code": "0204", "description": AuthConfig.login_code_map["0204"]}, 204

    if not UsersUtils.verify_password(plain_password=password,
                                      hashed_password=get_user_info["data"]["password"]):
        g.response_code = "0410"
        logger.critical(f"{request_id} - the password is incorrect")
        return {"code": "0410", "description": AuthConfig.login_code_map["0410"]}, 400

    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds)
    }

    token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)
    g.response_code = "0200"
    return {
        "code": "0200",
        "description": AuthConfig.login_code_map["0200"],
        "data": {
            "token": token,
            "user_id": get_user_info["data"]["user_id"]
        }
    }, 200

def login_otp(model, request_id):
    user_id = model["user_id"]
    otp_token = model["otp_token"]

    logger.info(f"{request_id} - user_id '{user_id}' is trying to login with otp '{otp_token}'...")
    result = AuthManager.login_otp(user_id=user_id,
                                   otp_token=otp_token,
                                   request_id=request_id)

    if not result["ok"]:
        g.response_code = "0500"
        logger.critical(f"{request_id} - database failed when this user tried to login with otp")
        return {"code": "0500", "description": AuthConfig.login_otp_code_map["0500"]}, 500

    if not result["data"]:
        g.response_code = "0204"
        logger.critical(f"{request_id} - invalid token or user_id")
        return {"code": "0204", "description": AuthConfig.login_otp_code_map["0204"]}, 204

    if result["data"]["expires_at"] < datetime.datetime.now():
        logger.info(f"{request_id} - user's otp_token is expired")
        g.response_code = "0410"
        return {"code": "0410", "description": AuthConfig.login_otp_code_map["0410"]}, 400

    logger.info(f"{request_id} - user's otp_token is valid, deleting used otp...")
    deleted = OtpManager.delete_otp(user_id=user_id,
                                    otp_token=otp_token,
                                    request_id=request_id)

    if not deleted["ok"]:
        logger.critical(f"{request_id} - database failed when deleting used otp_token")
        g.response_code = "0501"
        return {"code": "0501", "description": AuthConfig.login_otp_code_map["0501"]}, 500

    logger.info(f"{request_id} - user logged in successfully")
    g.response_code = "0200"
    return {
        "code": "0200",
        "description": AuthConfig.login_otp_code_map["0200"],
    }, 200
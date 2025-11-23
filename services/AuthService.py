import jwt

from flask import g
from configs.ServerConfig import logger

from utils import UsersUtils, AuthUtils
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

    user_id = get_user_info['data']['user_id']
    g.user_id = user_id
    logger.info(f"{request_id} - checking if user's account was banned...")
    if get_user_info['data']['is_banned']:
        logger.error(f"{request_id} - the user's account is banned")
        g.response_code = "0412"
        return {}

    logger.info(f"{request_id} - checking password...")
    if not UsersUtils.verify_password(plain_password=password, hashed_password=get_user_info["data"]["password"]):
        logger.error(f"{request_id} - the password is incorrect")
        g.response_code = "0410"
        return {}

    logger.info(f"{request_id} - checking if user's account was verified...")
    if not get_user_info['data']['email_verified']:
        logger.error(f"{request_id} - the user's account is not verified")
        g.response_code = "0411"
        return {}

    logger.info(f"{request_id} - updating user's last login...")
    last_login = AuthRepository.update_user_last_login(user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map={"database_error_code": "0501"})

    if last_login["error"]:
        return {}

    roles = get_user_info['data']['roles']
    token = AuthUtils.generate_jwt_token(user_id=user_id, roles=roles, request_id=request_id)
    g.response_code = "0200"
    return {
        "data": {
            "token": token
        }
    }

def refresh_token(user_id, request_id):
    logger.info(f"{request_id} - checking if needed to refresh jwt token...")
    decoded = AuthUtils.check_jwt_token()
    temp_response_code = "0200"

    if decoded["error"]:
        if not decoded["error_code"] == 0:
            logger.error(f"{request_id} - the requested jwt token is invalid")
            g.response_code = "0410"
            return {}
        else:
            logger.debug(f"{request_id} - the requested jwt token is valid and did not expire yet")
            temp_response_code = "0201"

    else:
        logger.debug(f"{request_id} - jwt token is expired (ok)")

    last_login = AuthRepository.update_user_last_login(user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map={"database_error_code": "0500"})

    if last_login["error"]:
        return {}

    token = AuthUtils.generate_jwt_token(user_id=user_id, roles=decoded["data"]["roles"], request_id=request_id)
    g.response_code = temp_response_code
    return {
        "data": {
            "token": token
        }
    }


def recover_account(model, request_id):
    username = model["username"]

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

    if not "new_password" in model:
        logger.info(f"{request_id} - request was only to only check if account exists...")

        logger.info(f"{request_id} - checking if account was banned...")
        if get_user_info['data']['is_banned']:
            logger.error(f"{request_id} - the account is banned")
            g.response_code = "0410"
            return {}

        g.response_code = "0201"
        return {}

    new_password = model["new_password"]
    hashed_password = UsersUtils.hash_password(plain_password=new_password)
    updated = AuthRepository.set_new_password(user_id=user_id,
                                              new_password=hashed_password,
                                              request_id=request_id,
                                              errors_code_map={"database_error_code": "0501"})

    if updated["error"]:
        return {}

    g.response_code = "0200"
    return {}

def confirm_account(model, request_id):
    username = model["username"]

    exists_username = UsersRepository.get_user_id_by_username(username=username,
                                                              request_id=request_id,
                                                              errors_code_map={
                                                                  "invalid_data_error_code": "0404",
                                                                  "database_error_code": "0500"
                                                              })

    if exists_username["error"]:
        return {}

    user_id = exists_username["data"]["id"]
    g.user_id = user_id

    isVerified = UsersRepository.check_user_verification_status_by_user_id(user_id=user_id,
                                                                           request_id=request_id,
                                                                           errors_code_map={
                                                                               "invalid_data_error_code": "0410",
                                                                               "database_error_code": "0501"
                                                                           })
    if isVerified["error"]:
        return {}

    verified = UsersRepository.mark_user_as_verified(user_id=user_id,
                                                     request_id=request_id,
                                                     errors_code_map={"database_error_code": "0502"})
    
    if verified["error"]:
        return {}

    g.response_code = "0200"
    return {}

def logout(user_id, request_id):
    logger.info(f"{request_id} - user '{user_id}' logged out successfully...")
    g.response_code = "0200"
    return {}
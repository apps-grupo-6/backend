from managers import AuthManager
from configs.ServerConfig import logger
from utils import ServerUtils

@ServerUtils.set_final_response
def get_username_info(username, request_id, errors_code_map):
    logger.info(f"{request_id} - obtaining '{username}' account information...")
    get_user_info = AuthManager.get_username_info(username=username, request_id=request_id)

    if not get_user_info["ok"]:
        logger.critical(f"{request_id} - an error occurred while obtaining user information")
        return {"flag": -1}

    if not get_user_info["data"]:
        logger.error(f"{request_id} - invalid username")
        return {"flag": 0}

    logger.debug(f"{request_id} - username exists")
    return {"flag": 1, "data": get_user_info['data']}

@ServerUtils.set_final_response
def check_otp_token(user_id, otp_token, type, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if user_id '{user_id}' has the otp_token '{otp_token}' with type '{type}'...")
    get_user_token = AuthManager.check_otp_token(user_id=user_id,
                                                 otp_token=otp_token,
                                                 type=type,
                                                 request_id=request_id)

    if not get_user_token["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking user otp_token")
        return {"flag": -1}

    if not get_user_token["data"]:
        logger.error(f"{request_id} - invalid otp_token, type or user_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - the requested otp_token exists for this user_id")
    return {"flag": 1, "data": get_user_token['data']}

# it's okay that this function does not use set_final_response decorator
def check_if_user_exists(user_id, request_id):
    logger.info(f"{request_id} - checking if user_id '{user_id}' exists our database...")
    get_user_token = AuthManager.check_if_user_exists(user_id=user_id,
                                                      request_id=request_id)

    return get_user_token

# it's okay that this function does not use set_final_response decorator
def set_new_password(user_id, new_password, request_id):
    logger.info(f"{request_id} - updating user_id '{user_id}' password...")
    updated = AuthManager.set_new_password(user_id=user_id,
                                           new_password=new_password,
                                           request_id=request_id)

    if not updated["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating")
        return False

    logger.debug(f"{request_id} - user password updated successfully")
    return True

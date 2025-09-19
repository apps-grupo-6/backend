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
def check_otp_token(user_id, otp_token, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if user_id '{user_id}' has the otp_token '{otp_token}'...")
    get_user_token = AuthManager.check_otp_token(user_id=user_id,
                                                 otp_token=otp_token,
                                                 request_id=request_id)

    if not get_user_token["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking user otp_token")
        return {"flag": -1}

    if not get_user_token["data"]:
        logger.error(f"{request_id} - invalid otp_token or user_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - the requested otp_token exists for this user_id")
    return {"flag": 1, "data": get_user_token['data']}

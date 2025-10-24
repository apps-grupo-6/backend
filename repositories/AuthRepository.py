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


# it's okay that this function does not use set_final_response decorator
def check_if_user_exists(user_id, request_id):
    get_user_data = AuthManager.check_if_user_exists(user_id=user_id,
                                                     request_id=request_id)

    return get_user_data

@ServerUtils.set_final_response
def update_user_last_login(user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - updating user_id '{user_id}' last login...")
    updated = AuthManager.update_user_last_login(user_id=user_id,
                                                 request_id=request_id)

    if not updated["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating")
        return {"flag": -1}

    logger.debug(f"{request_id} - user last login updated successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def set_new_password(user_id, new_password, request_id, errors_code_map):
    logger.info(f"{request_id} - updating user_id '{user_id}' password...")
    updated = AuthManager.set_new_password(user_id=user_id,
                                           new_password=new_password,
                                           request_id=request_id)

    if not updated["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating")
        return {"flag": -1}

    logger.debug(f"{request_id} - user password updated successfully")
    return {"flag": 1}
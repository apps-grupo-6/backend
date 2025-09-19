from managers import UsersManager
from configs.ServerConfig import logger
from utils import ServerUtils

@ServerUtils.set_final_response
def check_if_user_exists(user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if user_id '{user_id}' exists...")
    user_exists = UsersManager.does_user_exist(user_id=user_id, request_id=request_id)

    if not user_exists["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if not user_exists["data"]:
        logger.error(f"{request_id} - invalid user_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - user exists")
    return {"flag": 1, "data": user_exists['data']}

@ServerUtils.set_final_response
def get_user_contact_information(user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - retrieving user_id '{user_id}' contact information...")
    user_information = UsersManager.get_user_information(user_id=user_id,
                                                         request_id=request_id)

    if not user_information["ok"]:
        logger.critical(f"{request_id} - an error occurred while retrieving")
        return {"flag": -1}

    if not user_information["data"]:
        logger.critical(f"{request_id} - invalid user_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - user contact information retrieved successfully")
    return {"flag": 1, "data": user_information['data']}
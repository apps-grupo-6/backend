from managers import UsersManager
from configs.ServerConfig import logger
from utils import ServerUtils

@ServerUtils.set_final_response
def check_if_user_exists(user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if user_id '{user_id}' exists...")
    exists_user_id = UsersManager.does_user_exist(user_id=user_id, request_id=request_id)

    if not exists_user_id["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if not exists_user_id["data"]:
        logger.error(f"{request_id} - invalid user_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - user_id exists")
    return {"flag": 1, "data": exists_user_id['data']}

@ServerUtils.set_final_response
def get_user_contact_information(user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - retrieving user_id '{user_id}' contact information...")
    user_information = UsersManager.get_user_information(user_id=user_id,
                                                         request_id=request_id)

    if not user_information["ok"]:
        logger.critical(f"{request_id} - an error occurred while retrieving")
        return {"flag": -1}

    if not user_information["data"]:
        logger.error(f"{request_id} - invalid user_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - user contact information retrieved successfully")
    return {"flag": 1, "data": user_information['data']}

@ServerUtils.set_final_response
def register_user(username, hashed_password, first_name, last_name, telephone,
                  contact_email, request_id, errors_code_map):
    logger.info(f"{request_id} - trying to register username '{username}'...")
    registered = UsersManager.register_account(username=username,
                                               password=hashed_password,
                                               first_name=first_name,
                                               last_name=last_name,
                                               telephone=telephone,
                                               email=contact_email,
                                               request_id=request_id)

    if not registered["ok"]:
        logger.critical(f"{request_id} - an error occurred while registering")
        return {"flag": -1}

    logger.debug(f"{request_id} - user contact registered successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def check_if_username_doesnt_exist(username, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if username '{username}' does not exist...")
    exists_username = UsersManager.does_username_exist(username=username, request_id=request_id)

    if not exists_username["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if exists_username["data"]:
        logger.error(f"{request_id} - username exists")
        return {"flag": 0}

    logger.debug(f"{request_id} - username does not exist")
    return {"flag": 1, "data": exists_username['data']}
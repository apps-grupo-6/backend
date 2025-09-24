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
                  contact_email, verification_token, verification_expires_at, request_id, errors_code_map):
    logger.info(f"{request_id} - trying to register username '{username}' with verification...")
    registered = UsersManager.register_account(username=username,
                                               password=hashed_password,
                                               first_name=first_name,
                                               last_name=last_name,
                                               telephone=telephone,
                                               email=contact_email,
                                               verification_token=verification_token,
                                               verification_expires_at=verification_expires_at,
                                               request_id=request_id)

    if not registered["ok"]:
        logger.critical(f"{request_id} - an error occurred while registering")
        return {"flag": -1}

    logger.debug(f"{request_id} - user registered with verification successfully")
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

@ServerUtils.set_final_response
def update_user(update_columns, update_values, request_id, errors_code_map):
    logger.info(f"{request_id} - updating user_id '{update_values[-1]}'...")
    updated = UsersManager.update_user(update_columns=update_columns,
                                       update_values=update_values,
                                       request_id=request_id)

    if not updated["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating")
        return {"flag": -1}

    logger.debug(f"{request_id} - user updated successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def check_if_username_exists(username, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if username '{username}' exists...")
    exists_username = UsersManager.does_username_exist(username=username, request_id=request_id)

    if not exists_username["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if not exists_username["data"]:
        logger.error(f"{request_id} - username does not exist")
        return {"flag": 0}

    logger.debug(f"{request_id} - username exists")
    return {"flag": 1, "data": exists_username['data']}

@ServerUtils.set_final_response
def register_user_with_verification(username, hashed_password, first_name, last_name, telephone,
                                   contact_email, verification_token, verification_expires_at, request_id, errors_code_map):
    logger.info(f"{request_id} - trying to register username '{username}' with verification...")
    registered = UsersManager.register_account_with_verification(username=username,
                                                               password=hashed_password,
                                                               first_name=first_name,
                                                               last_name=last_name,
                                                               telephone=telephone,
                                                               email=contact_email,
                                                               verification_token=verification_token,
                                                               verification_expires_at=verification_expires_at,
                                                               request_id=request_id)

    if not registered["ok"]:
        logger.critical(f"{request_id} - an error occurred while registering")
        return {"flag": -1}

    logger.debug(f"{request_id} - user registered with verification successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def get_user_by_verification_code(username, verification_code, request_id, errors_code_map):
    logger.info(f"{request_id} - getting user by verification code for username '{username}'...")
    user_data = UsersManager.get_user_by_verification_code(username=username,
                                                         verification_code=verification_code,
                                                         request_id=request_id)

    if not user_data["ok"]:
        logger.critical(f"{request_id} - an error occurred while getting user")
        return {"flag": -1}

    if not user_data["data"]:
        logger.error(f"{request_id} - invalid username or verification code")
        return {"flag": 0}

    logger.debug(f"{request_id} - user found by verification code")
    return {"flag": 1, "data": user_data['data']}

@ServerUtils.set_final_response
def mark_user_as_verified(user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - marking user_id '{user_id}' as verified...")
    verified = UsersManager.mark_user_as_verified(user_id=user_id, request_id=request_id)

    if not verified["ok"]:
        logger.critical(f"{request_id} - an error occurred while marking as verified")
        return {"flag": -1}

    logger.debug(f"{request_id} - user marked as verified successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def get_user_id_by_username(username, request_id, errors_code_map):
    logger.info(f"{request_id} - getting user_id for username '{username}'...")
    user_data = UsersManager.does_username_exist(username=username, request_id=request_id)

    if not user_data["ok"]:
        logger.critical(f"{request_id} - an error occurred while getting user_id")
        return {"flag": -1}

    if not user_data["data"]:
        logger.error(f"{request_id} - username does not exist")
        return {"flag": 0}

    logger.debug(f"{request_id} - user_id retrieved successfully")
    return {"flag": 1, "data": user_data['data']}

@ServerUtils.set_final_response
def update_user_verification_token(user_id, verification_token, verification_expires_at, request_id, errors_code_map):
    logger.info(f"{request_id} - updating verification token for user_id '{user_id}'...")
    updated = UsersManager.update_user_verification_token(
        user_id=user_id,
        verification_token=verification_token,
        verification_expires_at=verification_expires_at,
        request_id=request_id
    )

    if not updated["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating verification token")
        return {"flag": -1}

    logger.debug(f"{request_id} - verification token updated successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def check_user_verification_status(username, request_id, errors_code_map):
    logger.info(f"{request_id} - checking verification status for username '{username}'...")
    user_status = UsersManager.get_user_verification_status(username=username, request_id=request_id)

    if not user_status["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking verification status")
        return {"flag": -1}

    if not user_status["data"]:
        logger.error(f"{request_id} - username does not exist")
        return {"flag": 0}

    if user_status["data"]["email_verified"]:
        logger.error(f"{request_id} - user is already verified")
        return {"flag": 0}

    logger.debug(f"{request_id} - user is not verified yet")
    return {"flag": 1, "data": user_status['data']}

@ServerUtils.set_final_response
def update_user_password(user_id, new_password, request_id, errors_code_map):
    logger.info(f"{request_id} - updating password for user_id '{user_id}'...")
    updated = UsersManager.update_user_password(
        user_id=user_id,
        new_password=new_password,
        request_id=request_id
    )

    if not updated["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating password")
        return {"flag": -1}

    logger.debug(f"{request_id} - password updated successfully")
    return {"flag": 1}

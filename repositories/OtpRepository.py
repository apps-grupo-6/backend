from managers import OtpManager
from configs.ServerConfig import logger
from utils import ServerUtils, OtpUtils

@ServerUtils.set_final_response
def check_if_user_has_active_otp(user_id, type, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if the user_id '{user_id}' already has an active '{type}' otp_token...")
    checked = OtpManager.check_if_user_has_active_otp(user_id=user_id,
                                                      type=type,
                                                      request_id=request_id)

    if not checked["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if checked["data"] and not OtpUtils.check_token_expired(checked=checked, request_id=request_id):
        logger.error(f"{request_id} - user already has an active otp_token with this type")
        return {"flag": 0, "data": checked['data']}

    logger.debug(f"{request_id} - user does not have an active otp_token with this type")
    return {"flag": 1, "data": checked['data']}

@ServerUtils.set_final_response
def save_otp(user_id, otp_token, type, request_id, errors_code_map):
    logger.info(f"{request_id} - saving otp_token for user_id '{user_id}'...")

    otp_token_saved = OtpManager.save_otp(otp_token=otp_token,
                                          user_id=user_id,
                                          type=type,
                                          request_id=request_id)

    if not otp_token_saved["ok"]:
        logger.critical(f"{request_id} - an error occurred while saving otp_token'")
        return {"flag": -1}

    logger.debug(f"{request_id} - otp_token saved successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def delete_otp(user_id, otp_token, type, request_id, errors_code_map):
    logger.info(f"{request_id} - deleting used otp_token '{otp_token}' with type '{type}' for user_id '{user_id}'...")
    deleted = OtpManager.delete_otp(user_id=user_id,
                                    otp_token=otp_token,
                                    type=type,
                                    request_id=request_id)

    if not deleted["ok"]:
        logger.critical(f"{request_id} - an error occurred while deleting used otp_token")
        return {"flag": -1}

    logger.debug(f"{request_id} - otp_token deleted successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def check_otp_token_by_username(username, otp_token, type, request_id, errors_code_map):
    logger.info(f"{request_id} - checking otp_token '{otp_token}' for username '{username}' with type '{type}'...")
    checked = OtpManager.check_otp_token_by_username(username=username,
                                                     otp_token=otp_token,
                                                     type=type,
                                                     request_id=request_id)

    if not checked["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking otp_token")
        return {"flag": -1}

    if not checked["data"]:
        logger.error(f"{request_id} - invalid otp_token")
        return {"flag": 0}

    logger.debug(f"{request_id} - otp_token is valid")
    return {"flag": 1, "data": checked['data']}

@ServerUtils.set_final_response
def check_otp_token_by_user_id(user_id, otp_token, type, request_id, errors_code_map):
    logger.info(f"{request_id} - checking otp_token '{otp_token}' for user_id '{user_id}' with type '{type}'...")
    checked = OtpManager.check_otp_token_by_user_id(user_id=user_id,
                                                    otp_token=otp_token,
                                                    type=type,
                                                    request_id=request_id)

    if not checked["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking otp_token")
        return {"flag": -1}

    if not checked["data"]:
        logger.error(f"{request_id} - invalid otp_token")
        return {"flag": 0}

    logger.debug(f"{request_id} - otp_token is valid")
    return {"flag": 1, "data": checked['data']}
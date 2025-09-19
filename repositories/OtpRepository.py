from managers import OtpManager
from configs.ServerConfig import logger
from utils import ServerUtils

@ServerUtils.set_final_response
def check_if_user_has_active_otp(user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if the user_id '{user_id}' already has an active otp token")
    checked = OtpManager.check_if_user_has_active_otp(user_id=user_id, request_id=request_id)

    if not checked["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    logger.debug(f"{request_id} - the user has an otp token associated")
    return {"flag": 1, "data": checked['data']}

@ServerUtils.set_final_response
def save_otp(user_id, otp_token, request_id, errors_code_map):
    logger.info(f"{request_id} - saving otp_token '{otp_token}' for user_id '{user_id}'...")

    otp_token_saved = OtpManager.save_otp(otp_token=otp_token,
                                          user_id=user_id,
                                          request_id=request_id)

    if not otp_token_saved["ok"]:
        logger.critical(f"{request_id} - an error occurred while saving otp_token'")
        return {"flag": -1}

    logger.debug(f"{request_id} - otp saved successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def delete_otp(user_id, otp_token, request_id, errors_code_map):
    logger.info(f"{request_id} - deleting used otp '{otp_token}' for user_id '{user_id}'...")
    deleted = OtpManager.delete_otp(user_id=user_id,
                                    otp_token=otp_token,
                                    request_id=request_id)

    if not deleted["ok"]:
        logger.critical(f"{request_id} - an error occurred while deleting used otp_token")
        return {"flag": -1}

    logger.debug(f"{request_id} - otp token deleted successfully")
    return {"flag": 1}
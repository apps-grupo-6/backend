from configs.ServerConfig import logger
from utils import ServerUtils

from managers import NotificationsManager

@ServerUtils.set_final_response
def set_user_token(user_id, expo_push_token, request_id, errors_code_map):
    logger.info(f"{request_id} - saving expo_push_token for user_id '{user_id}'...")
    expo_push_token_saved = NotificationsManager.set_user_token(expo_push_token=expo_push_token,
                                                                user_id=user_id,
                                                                request_id=request_id)

    if not expo_push_token_saved["ok"]:
        logger.critical(f"{request_id} - an error occurred while saving expo_push_token")
        return {"flag": -1}

    logger.debug(f"{request_id} - expo_push_token saved successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def get_class_participants_token(class_id, request_id, errors_code_map):
    logger.info(f"{request_id} - retrieving all expo_push_token for class_id '{class_id}'...")
    expo_push_tokens = NotificationsManager.get_class_participants_token(class_id=class_id, request_id=request_id)

    if not expo_push_tokens["ok"]:
        logger.critical(f"{request_id} - an error occurred while retrieving expo_push_tokens")
        return {"flag": -1}

    if not expo_push_tokens["data"]:
        logger.debug(f"{request_id} - no push notification will be send because this class_id has not any participants yet")
        return {"flag": 0}

    logger.debug(f"{request_id} - {len(expo_push_tokens['data'])} expo_push_tokens retrieved successfully")
    return {"flag": 1, "data": [row["expo_push_token"] for row in expo_push_tokens["data"]]}
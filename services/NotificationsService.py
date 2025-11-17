from flask import g

from configs.ServerConfig import logger
from repositories import NotificationsRepository
from utils import NotificationsUtils

def create_notification(model, request_id):
    notification_type = model["type"]
    class_id = model["class_id"]

    notification_data = NotificationsUtils.generate_notification_data(notification_type=notification_type,
                                                                      class_id=class_id,
                                                                      request_id=request_id,
                                                                      errors_code_map={
                                                                          "invalid_data_error_code": "0404",
                                                                          "database_error_code": "0500"
                                                                      })

    if notification_data["error"]:
        return {}

    users_to_notify = NotificationsRepository.get_class_participants_token(class_id=class_id,
                                                                           request_id=request_id,
                                                                           errors_code_map={
                                                                               "invalid_data_error_code": "0201",
                                                                               "database_error_code": "0501"
                                                                           })

    if users_to_notify["error"]:
        return {}

    g.send_push_notification_data = notification_data["data"]
    g.send_push_notification_users_token = users_to_notify["data"]["expo_push_token"]
    logger.info(users_to_notify["data"]["expo_push_token"])
    g.response_code = "0200"
    return {}

def set_user_token(model, user_id, request_id):
    expo_push_token = model["expo_push_token"]
    expo_push_token_saved = NotificationsRepository.set_user_token(user_id=user_id,
                                                                   expo_push_token=expo_push_token,
                                                                   request_id=request_id,
                                                                   errors_code_map={"database_error_code": "0500"})

    if expo_push_token_saved["error"]:
        return {}

    g.response_code = "0200"
    return {}


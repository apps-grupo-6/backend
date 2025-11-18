from flask import g

from repositories import NotificationsRepository

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


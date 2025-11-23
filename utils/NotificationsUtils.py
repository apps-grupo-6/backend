from flask import g

from configs.ServerConfig import logger
from repositories import NotificationsRepository

def generate_class_notification_data(notification_type, class_id, class_information, request_id):
    final_response = {
        "data": {
            "title": "",
            "body": "",
            "categoryId": notification_type,
            "data": {
                "class_id": class_id,
                "type": notification_type
            }
        }
    }
    logger.info(f"{request_id} - generating push notification '{notification_type}' for class_id '{class_id}'...")

    class_data = class_information["data"]
    professor_full_name = f"{class_data['professor_first_name']} {class_data['professor_last_name']}"
    gym_name = class_data['gym_name']
    class_discipline_name = class_data['class_discipline_name']
    day, hour = class_data["class_scheduled_at"].split(" ")

    if notification_type == "CLASS_CANCELLED":
        title = f"Tu clase de {class_discipline_name} fue cancelada"
        body = f"La clase del día {day} a las {hour} con {professor_full_name} en el {gym_name} fue cancelada."
    elif notification_type == "CLASS_RESCHEDULED":
        title = f"Tu clase de {class_discipline_name} fue reprogramada"
        body = f"La clase con {professor_full_name} en el {gym_name} se reprogramó para el día {day} a las {hour}."

    logger.debug(f"{request_id} - generated title: {title}")
    logger.debug(f"{request_id} - generated body: {body}")

    final_response["data"]["title"] = title
    final_response["data"]["body"] = body
    return final_response

def set_notifications_push(notification_type, class_id, class_information, request_id, errors_code_map):
    notification_data = generate_class_notification_data(notification_type=notification_type,
                                                         class_id=class_id,
                                                         class_information=class_information,
                                                         request_id=request_id)

    users_to_notify = NotificationsRepository.get_class_participants_token(class_id=class_id,
                                                                           request_id=request_id,
                                                                           errors_code_map=errors_code_map)

    if users_to_notify["error"]:
        return {"error": True}

    g.send_push_notification_data = notification_data["data"]
    g.send_push_notification_users_token = users_to_notify["data"]
    return {"error": False}
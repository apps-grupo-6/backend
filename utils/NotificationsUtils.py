from configs.ServerConfig import logger

from repositories import ClassesRepository

def generate_notification_data(notification_type, class_id, request_id, errors_code_map):
    final_response = {
        "error": False,
        "data": {
            "title": "",
            "body": ""
        }
    }

    logger.info(f"{request_id} - generating notification '{notification_type}' for class_id '{class_id}'...")

    class_information = ClassesRepository.get_class_information(class_id=class_id,
                                                                request_id=request_id,
                                                                errors_code_map=errors_code_map)

    if class_information["error"]:
        final_response["error"] = True
        return {}

    class_data = class_information["data"]
    professor_full_name = f"{class_data['professor']['first_name']} {class_data['professor']['last_name']}"
    gym_name = class_data['gym_name']
    class_discipline_name = class_data['class_discipline_name']
    day, hour = class_data["class_scheduled_at"].split(" ")

    if notification_type == "CLASS_CANCELLED":
        title = f"La clase de {class_discipline_name} fue cancelada"
        body = f"Tu clase del día {day} a las {hour} con {professor_full_name} en el {gym_name} fue cancelada."
    else:
        title = f"La clase de {class_discipline_name} fue reprogramada"
        body = f"Tu clase con {professor_full_name} en el {gym_name} se reprogramó para el día {day} a las {hour}."

    logger.debug(f"{request_id} - generated title: {title}")
    logger.debug(f"{request_id} - generated body: {body}")

    final_response["data"]["title"] = title
    final_response["data"]["body"] = body
    return final_response
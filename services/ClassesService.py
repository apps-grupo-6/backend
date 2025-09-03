from configs.ServerConfig import logger
from flask import g
import datetime

from managers import ClassesManager, UsersManager, LocationsManager, DisciplinesManager
from configs import ClassesConfig

def create_class(model, request_id):
    professor_id = model["professor_id"]
    location_id = model["location_id"]
    discipline_id = model["discipline_id"]
    scheduled_at = model["scheduled_at"]
    max_participants = model["max_participants"]
    qr = model["qr"]

    logger.info(f"{request_id} - validating if user_id '{professor_id}' exists...")
    user_exist = UsersManager.does_user_exist(user_id=professor_id, request_id=request_id)
    if not user_exist["ok"]:
        logger.critical(f"{request_id} - there was an error while checking")
        g.response_code = "0500"
        return {"code": "0500", "description": ClassesConfig.create_class_code_map["0500"]}, 500

    if not user_exist["data"]:
        logger.critical(f"{request_id} - invalid user_id")
        g.response_code = "0410"
        return {"code": "0410", "description": ClassesConfig.create_class_code_map["0410"]}, 400

    logger.info(f"{request_id} - validating if location_id '{location_id}' exists...")
    location_exist = LocationsManager.does_location_exist(location_id=location_id, request_id=request_id)
    if not location_exist["ok"]:
        logger.critical(f"{request_id} - there was an error while checking")
        g.response_code = "0501"
        return {"code": "0501", "description": ClassesConfig.create_class_code_map["0501"]}, 500

    if not location_exist["data"]:
        logger.critical(f"{request_id} - invalid location_id")
        g.response_code = "0411"
        return {"code": "0411", "description": ClassesConfig.create_class_code_map["0411"]}, 400

    logger.info(f"{request_id} - validating if discipline_id '{discipline_id}' exists...")
    discipline_exist = DisciplinesManager.does_disciplines_exist(discipline_id=discipline_id, request_id=request_id)
    if not discipline_exist["ok"]:
        logger.critical(f"{request_id} - there was an error while checking")
        g.response_code = "0502"
        return {"code": "0502", "description": ClassesConfig.create_class_code_map["0502"]}, 500

    if not discipline_exist["data"]:
        logger.critical(f"{request_id} - invalid discipline_id")
        g.response_code = "0412"
        return {"code": "0412", "description": ClassesConfig.create_class_code_map["0412"]}, 400

    logger.info(f"{request_id} - checking if exists a duplicated class with this data...")
    is_repeated = ClassesManager.check_if_repeated(professor_id=professor_id,
                                                   location_id=location_id,
                                                   discipline_id=discipline_id,
                                                   request_id=request_id)

    if not is_repeated["ok"]:
        logger.critical(f"{request_id} - there was an error while checking")
        g.response_code = "0503"
        return {"code": "0503", "description": ClassesConfig.create_class_code_map["0503"]}, 500

    if is_repeated["data"]:
        logger.info(f"{request_id} - there is a duplicated class")

        if not is_repeated["data"]["ended_at"]:
            logger.info(f"{request_id} - the class did not finish yet")
            scheduled_at_formatted = datetime.datetime.strptime(scheduled_at, "%Y-%m-%d %H:%M:%S")
            seconds_diff = scheduled_at_formatted - is_repeated["data"]["scheduled_at"]
            minutes_diff = seconds_diff.total_seconds() / 60

            if minutes_diff < 30:
                logger.error(f"{request_id} - to register the same class but different scheduled_at, you must send it with atleast 30 minutes difference")
                g.response_code = "0414"
                return {"code": "0414", "description": ClassesConfig.create_class_code_map["0414"]}, 400
        else:
            logger.info(f"{request_id} - the class is finished")
            g.response_code = "0413"
            return {"code": "0413", "description": ClassesConfig.create_class_code_map["0413"]}, 400

    logger.info(f"{request_id} - creating class..")
    created = ClassesManager.create_class(qr=qr,
                                          professor_id=professor_id,
                                          location_id=location_id,
                                          discipline_id=discipline_id,
                                          scheduled_at=scheduled_at,
                                          max_participants=max_participants,
                                          request_id=request_id)

    if not created["ok"]:
        logger.critical(f"{request_id} - there was an error while creating class")
        g.response_code = "0504"
        return {"code": "0504", "description": ClassesConfig.create_class_code_map["0504"]}, 500

    g.response_code = "0200"
    return {
        "code": "0200",
        "description": ClassesConfig.create_class_code_map["0200"]
    }, 200

def finish_class(model, request_id):
    class_id = model["class_id"]

    logger.info(f"{request_id} - validating if class_id '{class_id}' exists...")
    class_exist = ClassesManager.does_class_exist(class_id=class_id, request_id=request_id)
    if not class_exist["ok"]:
        logger.critical(f"{request_id} - there was an error while checking")
        g.response_code = "0500"
        return {"code": "0500", "description": ClassesConfig.finish_class_code_map["0500"]}, 500

    if not class_exist["data"]:
        logger.critical(f"{request_id} - invalid class_id")
        g.response_code = "0410"
        return {"code": "0410", "description": ClassesConfig.finish_class_code_map["0410"]}, 400

    if class_exist["data"]["ended_at"]:
        logger.info(f"{request_id} - class '{class_id}' is already finished")
        g.response_code = "0411"
        return {"code": "0411", "description": ClassesConfig.finish_class_code_map["0411"]}, 400

    finished_class = ClassesManager.finish_class(class_id=class_id, request_id=request_id)
    if not finished_class["ok"]:
        logger.critical(f"{request_id} - there was an error while checking")
        g.response_code = "0501"
        return {"code": "0501", "description": ClassesConfig.finish_class_code_map["0501"]}, 500

    logger.info(f"{request_id} - class finished successfully")
    g.response_code = "0200"
    return {
        "code": "0200",
        "description": ClassesConfig.finish_class_code_map["0200"]
    }, 200


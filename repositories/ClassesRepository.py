from managers import ClassesManager
from configs.ServerConfig import logger
from utils import ServerUtils

@ServerUtils.set_final_response
def check_if_class_exists(class_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if class_id '{class_id}' exists...")
    class_exists = ClassesManager.does_class_exist(class_id=class_id, request_id=request_id)

    if not class_exists["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if not class_exists["data"]:
        logger.error(f"{request_id} - invalid class_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - class_id exists")
    return {"flag": 1}

@ServerUtils.set_final_response
def get_class_info(class_id, request_id, errors_code_map):
    logger.info(f"{request_id} - retrieving class_id '{class_id}' information...")
    class_information = ClassesManager.get_class_information(class_id=class_id, request_id=request_id)

    if not class_information["ok"]:
        logger.critical(f"{request_id} - an error occurred while retrieving information")
        return {"flag": -1}

    if not class_information["data"]:
        logger.error(f"{request_id} - invalid class_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - class information retrieved successfully")
    return {"flag": 1, "data": class_information['data']}

@ServerUtils.set_final_response
def finish_class(class_id, request_id, errors_code_map):
    logger.info(f"{request_id} - finishing class_id '{class_id}'...")
    finished_class = ClassesManager.finish_class(class_id=class_id, request_id=request_id)

    if not finished_class["ok"]:
        logger.critical(f"{request_id} - an error occurred while finishing class")
        return {"flag": -1}

    logger.debug(f"{request_id} - class finished successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def check_if_duplicated(professor_id, location_id, discipline_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if exists a class with: {professor_id=} | {location_id=} | {discipline_id=}...")
    is_duplicated = ClassesManager.check_if_duplicated(professor_id=professor_id,
                                                       location_id=location_id,
                                                       discipline_id=discipline_id,
                                                       request_id=request_id)

    if not is_duplicated["ok"]:
        logger.critical(f"{request_id} - an error occurred while while checking")
        return {"flag": -1}

    if not is_duplicated["data"]:
        logger.debug(f"{request_id} - there's a duplicated class with this information")
    else:
        logger.debug(f"{request_id} - there isn't a duplicated class with this information")

    return {"flag": 1}

@ServerUtils.set_final_response
def create_class(qr, professor_id, location_id, discipline_id, scheduled_at,
                 max_participants, request_id, errors_code_map):
    logger.info(f"{request_id} - creating class...")
    created = ClassesManager.create_class(qr=qr,
                                          professor_id=professor_id,
                                          location_id=location_id,
                                          discipline_id=discipline_id,
                                          scheduled_at=scheduled_at,
                                          max_participants=max_participants,
                                          request_id=request_id)

    if not created["ok"]:
        logger.critical(f"{request_id} - an error occurred while creating class")
        return {"flag": -1}

    logger.debug(f"{request_id} - class created successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def update_class(update_columns, values, request_id, errors_code_map):
    logger.info(f"{request_id} - updating class...")
    updated = ClassesManager.update_class(update_columns=update_columns,
                                          update_values=values,
                                          request_id=request_id)
    if not updated["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating")
        return {"flag": -1}

    logger.debug(f"{request_id} - class updated successfully")
    return {"flag": 1}
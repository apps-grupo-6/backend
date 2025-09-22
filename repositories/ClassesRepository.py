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
def get_class_information(class_id, request_id, errors_code_map):
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
def check_if_duplicated(professor_id, location_id, discipline_id, scheduled_at, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if exists a class with: {professor_id=} | {location_id=} | {discipline_id=} | {scheduled_at=}...")
    is_duplicated = ClassesManager.check_if_duplicated(professor_id=professor_id,
                                                       location_id=location_id,
                                                       discipline_id=discipline_id,
                                                       scheduled_at=scheduled_at,
                                                       request_id=request_id)

    if not is_duplicated["ok"]:
        logger.critical(f"{request_id} - an error occurred while while checking")
        return {"flag": -1}

    if is_duplicated["data"]:
        logger.error(f"{request_id} - there's a duplicated class with this information")
        return {"flag": 0}

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
def update_class(update_columns, update_values, request_id, errors_code_map):
    logger.info(f"{request_id} - updating class_id '{update_values[-1]}'...")
    updated = ClassesManager.update_class(update_columns=update_columns,
                                          update_values=update_values,
                                          request_id=request_id)

    if not updated["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating")
        return {"flag": -1}

    logger.debug(f"{request_id} - class updated successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def get_all_classes(request_id, errors_code_map):
    # Created by Luciana
    logger.info(f"{request_id} - getting all classes...")
    classes_result = ClassesManager.get_all_classes(request_id=request_id)

    if not classes_result["ok"]:
        logger.critical(f"{request_id} - an error occurred while getting classes")
        return {"flag": -1}

    logger.debug(f"{request_id} - found {len(classes_result['data'])} classes")
    return {"flag": 1, "data": classes_result['data']}

@ServerUtils.set_final_response
def get_class_participants(class_id, request_id, errors_code_map):
    logger.info(f"{request_id} - getting all class_id '{class_id}' participants...")
    class_participants = ClassesManager.get_class_participants(class_id=class_id, request_id=request_id)

    if not class_participants["ok"]:
        logger.critical(f"{request_id} - an error occurred while getting class participants")
        return {"flag": -1}

    logger.debug(f"{request_id} - found {len(class_participants['data'])} participants")
    return {"flag": 1, "data": class_participants['data']}

@ServerUtils.set_final_response
def add_class_participant(class_id, user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - saving user_id '{user_id}' as class_id '{class_id}' participant...")
    added_participant = ClassesManager.add_class_participant(class_id=class_id,
                                                             user_id=user_id,
                                                             request_id=request_id)

    if not added_participant["ok"]:
        logger.critical(f"{request_id} - an error occurred while adding participant to class")
        return {"flag": -1}

    logger.debug(f"{request_id} - participant added successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def get_user_upcoming_classes(user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - retrieving all user_id '{user_id}' upcoming classes...")
    upcoming_classes = ClassesManager.get_user_upcoming_classes(user_id=user_id, request_id=request_id)

    if not upcoming_classes["ok"]:
        logger.critical(f"{request_id} - an error occurred while retrieving user upcoming classes")
        return {"flag": -1}

    logger.debug(f"{request_id} - user upcoming classes retrieved successfully")
    return {"flag": 1, "data": upcoming_classes['data']}

@ServerUtils.set_final_response
def update_participants_status(class_id, request_id, errors_code_map):
    logger.info(f"{request_id} - updating all class_id '{class_id}' participants' status, as it finished...")
    participant_status = ClassesManager.update_participants_status(class_id=class_id, request_id=request_id)

    if not participant_status["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating all participants' status")
        return {"flag": -1}

    logger.debug(f"{request_id} - participants' status was updated successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def cancel_participant(class_id, user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - trying to cancel participant with user_id '{user_id}' presence in class_id '{class_id}'...")
    participant_status = ClassesManager.cancel_participant(class_id=class_id,
                                                           user_id=user_id,
                                                           request_id=request_id)

    if not participant_status["ok"]:
        logger.critical(f"{request_id} - an error occurred while cancelling all participants' status")
        return {"flag": -1}

    if not participant_status["data"]:
        logger.error(f"{request_id} - user's status cannot be changed to 'CANCELLED'")
        return {"flag": 0}

    logger.debug(f"{request_id} - participant cancelled successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def confirm_participant(class_id, user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - trying to confirm participant with user_id '{user_id}' presence in class_id '{class_id}'...")
    participant_confirmed = ClassesManager.confirm_participant(class_id=class_id,
                                                               user_id=user_id,
                                                               request_id=request_id)

    if not participant_confirmed["ok"]:
        logger.critical(f"{request_id} - an error occurred while updating all participants' status")
        return {"flag": -1}

    if not participant_confirmed["data"]:
        logger.error(f"{request_id} - user's status cannot be changed to 'CONFIRMED'")
        return {"flag": 0}

    logger.debug(f"{request_id} - participant cancelled successfully")
    return {"flag": 1}

@ServerUtils.set_final_response
def check_if_participant_exists(class_id, user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if user_id '{user_id}' participates in class_id '{class_id}'...")
    class_exists = ClassesManager.does_participant_exist(class_id=class_id,
                                                         user_id=user_id,
                                                         request_id=request_id)

    if not class_exists["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if not class_exists["data"]:
        logger.error(f"{request_id} - user_id is not a participant in this class")
        return {"flag": 0}

    logger.debug(f"{request_id} - user_id is a participant in this class")
    return {"flag": 1}

@ServerUtils.set_final_response
def check_if_user_doesnt_participant(class_id, user_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if user_id '{user_id}' participates in class_id '{class_id}'...")
    exists_participant = ClassesManager.does_participant_exist(class_id=class_id,
                                                               user_id=user_id,
                                                               request_id=request_id)

    if not exists_participant["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if exists_participant["data"]:
        logger.error(f"{request_id} - user_id is already a participant in this class")
        return {"flag": 0}

    logger.debug(f"{request_id} - user_id is not a participant in this class")
    return {"flag": 1}

@ServerUtils.set_final_response
def get_user_classes_history(user_id, columns, values, request_id, errors_code_map):
    logger.info(f"{request_id} - retrieving all classes where user_id '{user_id}' has interacted...")
    user_history = ClassesManager.get_user_classes_history(user_id=user_id,
                                                                 columns=columns,
                                                                 column_values=values,
                                                                 request_id=request_id)

    if not user_history["ok"]:
        logger.critical(f"{request_id} - an error occurred while retrieving")
        return {"flag": -1}

    logger.debug(f"{request_id} - found {len(user_history['data'])} classes")
    return {"flag": 1, "data": user_history['data']}
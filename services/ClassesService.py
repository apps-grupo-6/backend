from configs.ServerConfig import logger
from flask import g
import datetime

from repositories import ClassesRepository, UserRepository, LocationsRepository, DisciplinesRepository
from utils import ClassesUtils

def create_class(model, request_id):
    professor_id = model["professor_id"]
    location_id = model["location_id"]
    discipline_id = model["discipline_id"]
    scheduled_at = model["scheduled_at"]
    max_participants = model["max_participants"]
    qr = model["qr"]

    is_duplicated = ClassesRepository.check_if_duplicated(professor_id=professor_id,
                                                          location_id=location_id,
                                                          discipline_id=discipline_id,
                                                          request_id=request_id,
                                                          errors_code_map={"database_error_code": "0503"})

    if is_duplicated["error"]:
        return {}

    if is_duplicated["data"]:
        if not is_duplicated["data"]["ended_at"]:
            logger.info(f"{request_id} - the class did not finish yet")
            scheduled_at_formatted = datetime.datetime.strptime(scheduled_at, "%Y-%m-%d %H:%M:%S")
            seconds_diff = scheduled_at_formatted - is_duplicated["data"]["scheduled_at"]
            minutes_diff = seconds_diff.total_seconds() / 60

            if minutes_diff < 30:
                logger.error(f"{request_id} - to register the same class but different scheduled_at, you must send it with at least 30 minutes difference")
                g.response_code = "0414"
                return {}
        else:
            logger.info(f"{request_id} - the class is finished")
            g.response_code = "0413"
            return {}


    exists_user = UserRepository.check_if_user_exists(user_id=professor_id,
                                                      request_id=request_id,
                                                      errors_code_map={
                                                          "database_error_code": "0500",
                                                          "invalid_data_error_code": "0410"
                                                      })

    if exists_user["error"]:
        return {}

    exists_location = LocationsRepository.check_if_location_exists(location_id=location_id,
                                                                   request_id=request_id,
                                                                   errors_code_map={
                                                                       "database_error_code": "0501",
                                                                       "invalid_data_error_code": "0411"
                                                                   })

    if exists_location["error"]:
        return {}

    exists_discipline = DisciplinesRepository.check_if_discipline_exists(discipline_id=discipline_id,
                                                                         request_id=request_id,
                                                                         errors_code_map={
                                                                             "database_error_code": "0502",
                                                                             "invalid_data_error_code": "0412"
                                                                         })

    if exists_discipline["error"]:
        return {}

    created_class = ClassesRepository.create_class(qr=qr,
                                                   professor_id=professor_id,
                                                   location_id=location_id,
                                                   discipline_id=discipline_id,
                                                   scheduled_at=scheduled_at,
                                                   max_participants=max_participants,
                                                   request_id=request_id,
                                                   errors_code_map={"database_error_code": "0504"})

    if created_class["error"]:
        return {}

    g.response_code = "0200"
    return {}

def finish_class(model, request_id):
    class_id = model["class_id"]

    class_information = ClassesUtils.check_and_get_class(class_id=class_id,
                                                         request_id=request_id,
                                                         error_code_maps={
                                                            "database_error_code": "0500",
                                                            "invalid_data_error_code": "0410"
                                                        })

    if not class_information:
        return {}

    if class_information["data"]["ended_at"]:
        logger.info(f"{request_id} - class already finished")
        g.response_code = "0412"
        return {}

    finished_class = ClassesRepository.finish_class(class_id=class_id,
                                                    request_id=request_id,
                                                    errors_code_map={"database_error_code": "0502"})

    if finished_class["error"]:
        return {}

    g.response_code = "0200"
    return {}

def update_class(model, request_id):
    class_id = model["class_id"]
    qr = model["qr"]
    columns = []
    values = []

    for key in model:
        if model[key] and key != "class_id":
            columns.append(f"{key} = %s")
            values.append(model[key])

    if not columns:
        logger.error(f"{request_id} - all updatable fields are empty")
        g.response_code = "0410"
        return {}

    class_information = ClassesUtils.check_and_get_class(class_id=class_id,
                                                         request_id=request_id,
                                                         error_code_maps={
                                                            "database_error_code": "0500",
                                                            "invalid_data_error_code": "0411"
                                                        })

    if not class_information:
        return {}

    if class_information["data"]["qr"] == qr:
        logger.info(f"{request_id} - sent qr is equal to actual class qr (if equal, there's no new data)")
        g.response_code = "0412"
        return {}

    update_columns = ", ".join(columns)
    values.append(class_id)
    updated = ClassesRepository.update_class(update_columns=update_columns,
                                             update_values=values,
                                             request_id=request_id,
                                             errors_code_map={"database_error_code": "0502"})

    if updated["error"]:
        return {}

    logger.info(f"{request_id} - class updated successfully")
    g.response_code = "0200"
    return {}


def get_all_classes(request_id):

    return None
import datetime

from configs.ServerConfig import logger
from flask import g

from repositories import ClassesRepository, UsersRepository, LocationsRepository, DisciplinesRepository
from utils import ClassesUtils

def get_all_classes(request_id):
    # Created by Luciana
    classes_result = ClassesRepository.get_all_classes(request_id=request_id,
                                                       errors_code_map={"database_error_code": "0500"})
    if classes_result["error"]:
        return {}

    classes_data = classes_result["data"] or []

    g.response_code = "0200"
    return {
        "data": classes_data
    }

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
                                                          scheduled_at=scheduled_at,
                                                          request_id=request_id,
                                                          errors_code_map={
                                                              "database_error_code": "0500",
                                                              "invalid_data_error_code": "0410"
                                                          })

    if is_duplicated["error"]:
        return {}

    exists_user = UsersRepository.check_if_user_exists(user_id=professor_id,
                                                       request_id=request_id,
                                                       errors_code_map={
                                                           "database_error_code": "0501",
                                                           "invalid_data_error_code": "0404"
                                                       })

    if exists_user["error"]:
        return {}

    exists_location = LocationsRepository.check_if_location_exists(location_id=location_id,
                                                                   request_id=request_id,
                                                                   errors_code_map={
                                                                       "database_error_code": "0502",
                                                                       "invalid_data_error_code": "0405"
                                                                   })

    if exists_location["error"]:
        return {}

    exists_discipline = DisciplinesRepository.check_if_discipline_exists(discipline_id=discipline_id,
                                                                         request_id=request_id,
                                                                         errors_code_map={
                                                                             "database_error_code": "0503",
                                                                             "invalid_data_error_code": "0406"
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

def get_user_upcoming_classes(user_id, request_id):
    upcoming_user_classes = ClassesRepository.get_user_upcoming_classes(user_id=user_id,
                                                                        request_id=request_id,
                                                                        errors_code_map={"database_error_code": "0500"})
    if upcoming_user_classes["error"]:
        return {}

    g.response_code = "0200"
    return {
        "data": upcoming_user_classes["data"]
    }

def get_class(class_id, request_id):
    class_information = ClassesUtils.check_and_get_class_information(class_id=class_id,
                                                                     request_id=request_id,
                                                                     error_code_maps={
                                                                         "database_error_code": "0500",
                                                                         "invalid_data_error_code": "0404"
                                                                     })

    if class_information["error"]:
        return {}

    g.response_code = "0200"
    return {
        "data": class_information["data"] or []
    }

def update_class(model, class_id, user_id, request_id):
    qr = model["qr"]

    class_information = ClassesUtils.check_and_get_class_information(class_id=class_id,
                                                                     request_id=request_id,
                                                                     error_code_maps={
                                                                         "database_error_code": "0500",
                                                                         "invalid_data_error_code": "0404"
                                                                     })

    if class_information["error"]:
        return {}

    professor_id = class_information["data"]["professor_id"]
    if not user_id == professor_id:
        g.alert_description = f"user_id '{user_id}' tried to update class '{class_id}' which professor_id is '{professor_id}'"
        logger.critical(f"{request_id} - [SECURITY BREACH] {g.alert_description}")
        g.response_code = "9999"
        return {}

    logger.info(f"{request_id} - formatting fields...")
    formatted_update = ClassesUtils.update_class_fields_formatter(model=model, request_id=request_id)
    error = formatted_update["error"]
    columns = formatted_update["columns"]
    values = formatted_update["values"]

    if error:
        return {}

    if not columns:
        logger.error(f"{request_id} - all updatable fields are empty")
        g.response_code = "0410"
        return {}

    if "scheduled_at" in model:
        if model["scheduled_at"] <= class_information["data"]["scheduled_at"]:
            logger.error(f"{request_id} - scheduled_at cannot be earlier than the current scheduled_at")
            g.response_code = "0412"
            return {}

        if model["scheduled_at"] < datetime.datetime.now():
            logger.error(f"{request_id} - scheduled_at cannot be in the past")
            g.response_code = "0413"
            return {}

    if "max_participants" in model:
        participants = ClassesRepository.get_class_participants(class_id=class_id,
                                                                request_id=request_id,
                                                                errors_code_map={"database_error_code": "0504"})

        if participants["error"]:
            return {}

        if model["max_participants"] > len(participants["data"]):
            logger.error(f"{request_id} - max_participants cannot be greater than the number of participants")
            g.response_code = "0414"
            return {}

    if class_information["data"]["qr"] == qr:
        logger.error(f"{request_id} - sent qr is equal to actual class qr (if equal, there's no new data)")
        g.response_code = "0411"
        return {}

    update_columns = ", ".join(columns)
    values.append(class_id)
    logger.debug(f"{request_id} - columns to update: {update_columns}")
    updated = ClassesRepository.update_class(update_columns=update_columns,
                                             update_values=values,
                                             request_id=request_id,
                                             errors_code_map={"database_error_code": "0505"})

    if updated["error"]:
        return {}

    g.response_code = "0200"
    return {}

def finish_class(class_id, user_id, request_id):
    class_information = ClassesUtils.check_and_get_class_information(class_id=class_id,
                                                                     request_id=request_id,
                                                                     error_code_maps={
                                                                         "database_error_code": "0500",
                                                                         "invalid_data_error_code": "0404"
                                                                     })

    if class_information["error"]:
        return {}

    professor_id = class_information["data"]["professor_id"]
    if not professor_id == user_id:
        g.alert_description = f"user_id '{user_id}' tried to finish class_id '{class_id}' which professor_id is '{professor_id}'"
        logger.critical(f"{request_id} - [SECURITY BREACH] {g.alert_description}")
        g.response_code = "9999"
        return {}

    if class_information["data"]["ended_at"]:
        logger.error(f"{request_id} - class already finished")
        g.response_code = "0410"
        return {}

    participants_status = ClassesRepository.update_participants_status(class_id=class_id,
                                                                       request_id=request_id,
                                                                       errors_code_map={"database_error_code": "0501"})

    if participants_status["error"]:
        return {}

    finished_class = ClassesRepository.finish_class(class_id=class_id,
                                                    request_id=request_id,
                                                    errors_code_map={"database_error_code": "0502"})

    if finished_class["error"]:
        return {}

    g.response_code = "0200"
    return {}

def add_class_participant(class_id, user_id, request_id):
    class_information = ClassesUtils.check_and_get_class_information(class_id=class_id,
                                                                     request_id=request_id,
                                                                     error_code_maps={
                                                                         "database_error_code": "0500",
                                                                         "invalid_data_error_code": "0404"
                                                                     })

    if class_information["error"]:
        return {}

    if class_information["data"] and datetime.datetime.fromisoformat(class_information["data"]["scheduled_at"]) <= datetime.datetime.now():
        logger.error(f"{request_id} - the class already started")
        g.response_code = "0410"
        return {}

    exists_participant = ClassesRepository.check_if_user_doesnt_participant(class_id=class_id,
                                                                            user_id=user_id,
                                                                            request_id=request_id,
                                                                            errors_code_map={
                                                                                "database_error_code": "0501",
                                                                                "invalid_data_error_code": "0405"
                                                                            })

    if exists_participant["error"]:
        return {}

    class_participants = ClassesRepository.get_class_participants(class_id=class_id,
                                                                  request_id=request_id,
                                                                  errors_code_map={"database_error_code": "0502"})
    if class_participants["error"]:
        return {}

    if class_participants["data"] and (len(class_participants["data"]) >= class_information["data"]["max_participants"]):
        logger.error(f"{request_id} - the class is full")
        g.response_code = "0411"
        return {}

    added_participant = ClassesRepository.add_class_participant(class_id=class_id,
                                                                user_id=user_id,
                                                                request_id=request_id,
                                                                errors_code_map={"database_error_code": "0503"})

    if added_participant["error"]:
        return {}

    g.response_code = "0200"
    return {}

def cancel_participant(class_id, user_id, request_id):
    exists_class = ClassesRepository.check_if_class_exists(class_id=class_id,
                                                           request_id=request_id,
                                                           errors_code_map={
                                                               "database_error_code": "0500",
                                                               "invalid_data_error_code": "0404"
                                                           })

    if exists_class["error"]:
        return {}

    exists_participant = ClassesRepository.check_if_participant_exists(class_id=class_id,
                                                                       user_id=user_id,
                                                                       request_id=request_id,
                                                                       errors_code_map={
                                                                           "database_error_code": "0501",
                                                                           "invalid_data_error_code": "0405",
                                                                       })

    if exists_participant["error"]:
        return {}

    cancel_user = ClassesRepository.cancel_participant(class_id=class_id,
                                                       user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map={
                                                           "database_error_code": "0501",
                                                           "invalid_data_error_code": "0406"
                                                       })

    if cancel_user["error"]:
        return {}

    g.response_code = "0200"
    return {}

def confirm_participant(class_id, user_id, request_id):
    exists_class = ClassesRepository.check_if_class_exists(class_id=class_id,
                                                           request_id=request_id,
                                                           errors_code_map={
                                                               "database_error_code": "0500",
                                                               "invalid_data_error_code": "0404"
                                                           })
    if exists_class["error"]:
        return {}

    exists_participant = ClassesRepository.check_if_participant_exists(class_id=class_id,
                                                                       user_id=user_id,
                                                                       request_id=request_id,
                                                                       errors_code_map={
                                                                           "database_error_code": "0501",
                                                                           "invalid_data_error_code": "0405",
                                                                       })

    if exists_participant["error"]:
        return {}

    confirm_user = ClassesRepository.confirm_participant(class_id=class_id,
                                                         user_id=user_id,
                                                         request_id=request_id,
                                                         errors_code_map={
                                                             "database_error_code": "0501",
                                                             "invalid_data_error_code": "0406"
                                                         })

    if confirm_user["error"]:
        return {}

    g.response_code = "0200"
    return {}

def get_user_classes_history(user_id, since, until, request_id):
    if since:
        since_date = ClassesUtils.validate_date(since)

        if not since_date:
            logger.error(f"{request_id} - since date '{since}' is invalid")
            g.response_code = "0400"
            return {}

    if until:
        until_date = ClassesUtils.validate_date(until)

        if not until_date:
            logger.error(f"{request_id} - until date '{until}' is invalid")
            g.response_code = "0400"
            return {}

        if since_date > until_date:
            logger.error(f"{request_id} - 'since' ({since}) cannot be later than 'until' ({until})")
            g.response_code = "0400"
            return {}

    data = {"since": since, "until": until}

    formatted_update = ClassesUtils.get_user_classes_formatter(model=data, request_id=request_id)
    error = formatted_update["error"]
    columns = formatted_update["columns"]
    values = formatted_update["values"]

    if error:
        return {}

    match_dates = " AND ".join(columns) if len(columns) else ""
    logger.debug(f"{request_id} - dates to match: {match_dates or None}")

    history = ClassesRepository.get_user_classes_history(user_id=user_id,
                                                         columns=match_dates,
                                                         values=values,
                                                         request_id=request_id,
                                                         errors_code_map={"database_error_code": "0500"})

    if history["error"]:
        return {}

    g.response_code = "0200"
    return {
        "data": history['data']
    }
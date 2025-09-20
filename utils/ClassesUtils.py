from datetime import datetime

from repositories import ClassesRepository

def check_and_get_class(class_id, request_id, error_code_maps):
    exists_class = ClassesRepository.check_if_class_exists(
        class_id=class_id,
        request_id=request_id,
        errors_code_map=error_code_maps
    )

    if exists_class["error"]:
        return {"error": True}

    class_information = ClassesRepository.get_class_information(
        class_id=class_id,
        request_id=request_id,
        errors_code_map=error_code_maps
    )

    if class_information["error"]:
        return {"error": True}

    return class_information

def check_if_class_finished(class_id, request_id, errors_code_maps):
    class_information = check_and_get_class(class_id=class_id,
                                            request_id=request_id,
                                            error_code_maps=errors_code_maps)

    if class_information["error"]:
        return {"error": True}

    if class_information["data"]["ended_at"] or class_information["data"]:
        return {"error": False}
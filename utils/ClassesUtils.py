from repositories import ClassesRepository

def check_and_get_class_information(class_id, request_id, error_code_maps):
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
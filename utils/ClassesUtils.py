import datetime

from repositories import ClassesRepository
from configs import ClassesConfig

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

def update_class_fields_formatter(model, request_id):
    columns = []
    values = []
    error = False

    for key in model:
        if key in ClassesConfig.update_class_fields_to_check:
            checking = ClassesConfig.update_class_fields_to_check[key]
            call = checking["function"](model[key],
                                        request_id=request_id,
                                        errors_code_map=checking["on_error"])

            if call["error"]:
                error = True
                break

        columns.append(f"{key} = %s")
        values.append(model[key])

    return {
        "error": error,
        "columns": columns,
        "values": values
    }

def get_user_classes_formatter(model, request_id):
    columns = []
    values = []
    error = False

    for key in model:
        if model[key]:
            comparing = ">=" if key == "since" else "<="
            columns.append(f"c.scheduled_at {comparing} %s")
            values.append(f"'{model[key]} 00:00:00'")

    return {
        "error": error,
        "columns": columns,
        "values": values
    }

def validate_date(date):
    print(date)
    if not ClassesConfig.DATE_REGEX.match(date):
        print("Date is not valid")
        return False
    print("Date is valid")

    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False
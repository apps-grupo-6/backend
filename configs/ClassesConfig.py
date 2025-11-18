import re

from repositories import LocationsRepository, DisciplinesRepository

BLOCKED_STATUS = ('EXPIRED', 'ABSENT', 'PRESENT', 'CANCELLED')
BLOCK_CONFIRM_STATUS = BLOCKED_STATUS + ('CONFIRMED',)

# thank you gpt for this regex
DATE_REGEX = re.compile("^\d{4}-(?:(?:0[13578]|1[02])-(0[1-9]|[12]\d|3[01])|(?:0[469]|11)-(0[1-9]|[12]\d|30)|02-(0[1-9]|1\d|2\d))$")

update_class_fields_to_check = {
    "location_id": {
        "function": LocationsRepository.check_if_location_exists,
        "on_error": {
            "database_error_code": "0502",
            "invalid_data_error_code": "0406"
        }
    },
    "discipline_id": {
        "function": DisciplinesRepository.check_if_discipline_exists,
        "on_error": {
            "database_error_code": "0503",
            "invalid_data_error_code": "0407"
        }
    }
}

get_all_classes_code_map = {
    "0200": ("ok", 200),
    "0500": ("the request could not be processed", 500)
}

create_class_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid professor_id", 404),
    "0405": ("invalid location_id", 404),
    "0406": ("invalid discipline_id", 404),
    "0410": ("there is an existent class with this data", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500),
    "0503": ("the request could not be processed", 500),
    "0504": ("the request could not be processed", 500)
}

upcoming_classes_code_map = {
    "0200": ("ok", 200),
    "0500": ("the request could not be processed", 500),
}

get_class_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid class_id", 404),
    "0500": ("the request could not be processed", 500)
}

update_class_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid class_id", 404),
    "0405": ("invalid user_id", 404),
    "0406": ("invalid location_id", 404),
    "0407": ("invalid discipline_id", 404),
    "0410": ("all updatable fields are empty", 400),
    "0411": ("there is no difference between sent qr and the actual one", 400),
    "0412": ("scheduled_at cannot be earlier than the current scheduled_at", 400),
    "0413": ("scheduled_at cannot be in the past", 400),
    "0414": ("max_participants cannot be greater than the number of participants", 400),
    "0415": ("this class_id was already cancelled", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500),
    "0503": ("the request could not be processed", 500),
    "0504": ("the request could not be processed", 500),
    "0505": ("the request could not be processed", 500)
}

finish_class_code_map = {
    "0200": ("ok", 200),
    "0404": ("invalid class_id", 404),
    "0410": ("the requested class is already finished", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500),
    "0503": ("the request could not be processed", 500)
}

add_participant_code_map = {
    "0200": ("ok", 200),
    "0404": ("invalid class_id", 404),
    "0405": ("the requested user is not a participant in this class", 404),
    "0410": ("the requested class already started", 400),
    "0411": ("the requested class_id is full", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500),
    "0503": ("the request could not be processed", 500)
}

cancel_participant_code_map = {
    "0200": ("ok", 200),
    "0404": ("invalid class_id", 404),
    "0405": ("the requested user is not a participant in this class", 404),
    "0406": ("the requested user has a status that cannot be changed to 'CANCELLED'", 404),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

confirm_participant_code_map = {
    "0200": ("ok", 200),
    "0404": ("invalid class_id", 404),
    "0405": ("the requested user is not a participant in this class", 404),
    "0406": ("the requested user has a status that cannot be changed to 'CONFIRMED'", 404),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

get_user_classes_history_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0500": ("the request could not be processed", 500)
}

start_class_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid class_id", 404),
    "0410": ("the requested class is already finished", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500)
}

cancel_class_code_map = {
    "0200": ("ok", 200),
    "0201": ("ok", 200),
    "0404": ("invalid class_id", 404),
    "0405": ("invalid class_id", 404),
    "0410": ("a finished class can not be cancelled", 400),
    "0411": ("the requested class is already cancelled", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500),
    "0503": ("the request could not be processed", 500)
}

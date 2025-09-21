BLOCKED_STATUS = ('EXPIRED', 'ABSENT', 'PRESENT', 'CANCELLED')
BLOCK_CONFIRM_STATUS = BLOCKED_STATUS + ('CONFIRMED',)

get_all_classes_code_map = {
    "0200": ("ok", 200),
    "0500": ("the request could not be processed", 500)
}

create_class_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0404": ("invalid user_id", 404),
    "0405": ("invalid location_id", 404),
    "0406": ("invalid discipline_id", 404),
    "0413": ("there is a class with this data", 400),
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
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500),
    "0503": ("the request could not be processed", 500)
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

add_class_participant_code_map = {
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
create_class_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0410": ("invalid user_id", 400),
    "0411": ("invalid location_id", 400),
    "0412": ("invalid discipline_id", 400),
    "0413": ("duplicated data in a finished class", 400),
    "0414": ("duplicated classes can only be created if requested at least 30 minutes apart", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500),
    "0503": ("the request could not be processed", 500),
    "0504": ("the request could not be processed", 500)
}

finish_class_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0410": ("invalid class_id", 400),
    "0411": ("invalid class_id", 400),
    "0412": ("the class_id is already finished", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

update_class_code_map = {
    "0200": ("ok", 200),
    "0400": ("bad request", 400),
    "0410": ("all updatable fields are empty", 400),
    "0411": ("invalid class_id", 400),
    "0412": ("there is no difference between sent qr and the actual one", 400),
    "0500": ("the request could not be processed", 500),
    "0501": ("the request could not be processed", 500),
    "0502": ("the request could not be processed", 500)
}

get_all_classes_code_map = {
    "0200": ("ok", 200),
    "0500": ("the request could not be processed", 500)
}
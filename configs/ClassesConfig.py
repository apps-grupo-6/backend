create_class_code_map = {
    "0200": "ok",
    "0204": "invalid username or otp_token",
    "0400": "bad request",
    "0410": "invalid user_id",
    "0411": "invalid location_id",
    "0412": "invalid discipline_id",
    "0413": "duplicated data in a finished class",
    "0414": "duplicated data without 30 minutes difference",
    "0500": "the request could not be processed",
    "0501": "the request could not be processed",
    "0502": "the request could not be processed",
    "0503": "the request could not be processed",
    "0504": "the request could not be processed"
}

finish_class_code_map = {
    "0200": "ok",
    "0400": "bad request",
    "0410": "invalid class_id",
    "0411": "the class_id is already finished",
    "0500": "the request could not be processed",
    "0501": "the request could not be processed",
    "0502": "the request could not be processed"
}

update_class_code_map = {
    "0200": "ok",
    "0400": "bad request",
    "0410": "all updatable fields are empty",
    "0411": "invalid class_id",
    "0500": "the request could not be processed",
    "0501": "the request could not be processed"
}
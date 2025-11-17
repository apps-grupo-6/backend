from flask import g
from configs.ServerConfig import logger

from repositories import UsersRepository
from utils import UsersUtils

def register_account(model, request_id):
    username = model["username"]
    password = model["password"].strip()
    first_name = model["first_name"]
    last_name = model["last_name"]
    telephone = model["telephone"]
    contact_email = model["contact_email"]

    exists_user = UsersRepository.check_if_username_doesnt_exist(username=username,
                                                                 request_id=request_id,
                                                                 errors_code_map={
                                                                     "database_error_code": "0500",
                                                                     "invalid_data_error_code": "0410"
                                                                 })
    if exists_user["error"]:
        return {}

    hashed_password = UsersUtils.hash_password(password)
    registered = UsersRepository.register_user(username=username,
                                               hashed_password=hashed_password,
                                               first_name=first_name,
                                               last_name=last_name,
                                               telephone=telephone,
                                               contact_email=contact_email,
                                               request_id=request_id,
                                               errors_code_map={"database_error_code": "0501"})

    if registered["error"]:
        return {}

    user_id = registered["data"]["user_id"]
    g.user_id = user_id
    logger.info(f"{request_id} - user registered with id: '{user_id}'")
    g.response_code = "0200"
    return {}

def update_user_information(model, user_id, request_id):
    logger.info(f"{request_id} - formatting fields...")
    formatted_update = UsersUtils.update_class_fields_formatter(model=model)

    error = formatted_update["error"]
    columns = formatted_update["columns"]
    values = formatted_update["values"]

    if error:
        return {}

    if not columns:
        logger.error(f"{request_id} - all updatable fields are empty")
        g.response_code = "0410"
        return {}

    update_columns = ", ".join(columns)
    values.append(user_id)
    logger.debug(f"{request_id} - columns to update: {update_columns}")
    updated = UsersRepository.update_user(update_columns=update_columns,
                                          update_values=values,
                                          request_id=request_id,
                                          errors_code_map={"database_error_code": "0500"})

    if updated["error"]:
        return {}

    g.response_code = "0200"
    return {}

def get_user_information(user_id, request_id):
    user_information = UsersRepository.get_user_contact_information(user_id=user_id,
                                                                    request_id=request_id,
                                                                    errors_code_map={"database_error_code": "0500"})

    if user_information["error"]:
        return {}

    g.response_code = "0200"
    return {
        "data": user_information['data']
    }
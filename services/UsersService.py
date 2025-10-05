from flask import g
from configs.ServerConfig import logger

from repositories import UsersRepository
from utils import UsersUtils, OtpUtils
from templates import OtpTemplate

def register_account(model, request_id):
    username = model["username"]
    password = model["password"].strip()
    first_name = model["first_name"]
    last_name = model["last_name"]
    telephone = model["telephone"]
    contact_email = model["contact_email"]
    hashed_password = UsersUtils.hash_password(password)
    TYPE = "REGISTRATION"

    exists_user = UsersRepository.check_if_username_doesnt_exist(username=username,
                                                                 request_id=request_id,
                                                                 errors_code_map={
                                                                     "database_error_code": "0500",
                                                                     "invalid_data_error_code": "0410"
                                                                 })
    if exists_user["error"]:
        return {}

    otp_token = OtpUtils.generate_otp(otp_type=TYPE, request_id=request_id)
    verification_token = otp_token["otp_token"]
    expires_at = otp_token["expires_at"]

    registered = UsersRepository.register_user(username=username,
                                               hashed_password=hashed_password,
                                               first_name=first_name,
                                               last_name=last_name,
                                               telephone=telephone,
                                               contact_email=contact_email,
                                               verification_token=verification_token,
                                               verification_expires_at=expires_at,
                                               request_id=request_id,
                                               errors_code_map={"database_error_code": "0501"})

    if registered["error"]:
        return {}

    user_id = registered["data"]["user_id"]
    logger.info(f"{request_id} - user registered with id: '{user_id}'")
    g.user_id = user_id

    g.send_email_data = {
        "subject": "Verifica tu cuenta - Código de activación",
        "user_email": contact_email,
        "user_firstname": first_name,
        "user_lastname": last_name,
        "html_content": OtpTemplate.render_registration_verification_email(first_name=first_name,
                                                                           last_name=last_name,
                                                                           username=username,
                                                                           otp_code=verification_token)
    }

    logger.info(f"{request_id} - verification email sent")

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
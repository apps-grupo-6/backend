from flask import g
from configs.ServerConfig import logger

from repositories import UsersRepository
from utils import UsersUtils
from templates import UserTemplate

def register_account(model, request_id):
    username = model["username"]
    password = model["password"].strip()
    first_name = model["first_name"]
    last_name = model["last_name"]
    telephone = model["telephone"]
    contact_email = model["contact_email"]
    hashed_password = UsersUtils.hash_password(password)

    exists_user = UsersRepository.check_if_username_doesnt_exist(username=username,
                                                                 request_id=request_id,
                                                                 errors_code_map={
                                                                     "database_error_code": "0500",
                                                                     "invalid_data_error_code": "0410"
                                                                 })
    if exists_user["error"]:
        return {}

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

    g.send_email_data = {
        "subject": "¡Bienvenido/a a Excuses 404!",
        "user_email": contact_email,
        "user_firstname": first_name,
        "user_lastname": last_name,
        "html_content": UserTemplate.render_register_email(first_name=first_name,
                                                           last_name=last_name,
                                                           username=username)
    }
    logger.info(f"{request_id} - username registered successfully")
    g.response_code = "0200"
    return {}
from flask import g
from configs.ServerConfig import logger

from managers import UsersManager
from configs import UsersConfig
from utils import UsersUtils

def register_account(model, request_id):
    username = model["username"]
    password = model["password"].strip()
    first_name = model["first_name"]
    last_name = model["last_name"]
    telephone = model["telephone"]
    contact_email = model["contact_email"]
    hashed_password = UsersUtils.hash_password(password)

    logger.info(f"{request_id} - trying to register username '{username}'...")
    registered = UsersManager.register_account(username=username,
                                               password=hashed_password,
                                               first_name=first_name,
                                               last_name=last_name,
                                               telephone=telephone,
                                               email=contact_email,
                                               request_id=request_id)

    if not registered["ok"]:
        g.response_code = "0500"
        logger.critical(f"{request_id} - database failed when trying register this user")
        return {"code": "0500", "description": UsersConfig.register_account_code_map["0500"]}, 500

    logger.info(f"{request_id} - username registered successfully")
    g.response_code = "0200"
    return {
        "code": "0200",
        "description": UsersConfig.register_account_code_map["0200"]
    }, 200
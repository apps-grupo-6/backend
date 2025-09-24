from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from services import UsersService
from models import UsersModel
from configs import UsersConfig
from utils import ServerUtils, AuthUtils

bp = Blueprint('users', __name__)

@bp.post("/")
@ServerUtils.configure_request(description_code_map=UsersConfig.register_account_code_map, method="POST")
def register_account():
    try:
        logger.info(f"{g.request_id} - starting register_account")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = UsersModel.register_account().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return UsersService.register_account(model=model, request_id=g.request_id)

@bp.get("/")
@ServerUtils.configure_request(description_code_map=UsersConfig.get_user_information_code_map, method="GET")
@AuthUtils.validate_session
def get_user_information():
    logger.info(f"{g.request_id} - starting get_user_information")
    return UsersService.get_user_information(user_id=g.user_id, request_id=g.request_id)

@bp.put("/")
@ServerUtils.configure_request(description_code_map=UsersConfig.update_user_information_code_map, method="PUT")
@AuthUtils.validate_session
def update_user_information():
    try:
        logger.info(f"{g.request_id} - starting update_user_information")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = UsersModel.update_user_information().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return UsersService.update_user_information(model=model, user_id=g.user_id, request_id=g.request_id)

@bp.post("/verify")
@ServerUtils.configure_request(description_code_map=UsersConfig.verify_registration_code_map, method="POST", endpoint="verify")
def verify_registration():
    try:
        logger.info(f"{g.request_id} - starting verify_registration")

        data = request.json
        username = data.get("username")
        verification_code = data.get("verification_code")
        
        if not username or not verification_code:
            g.response_code = "0400"
            return {
                "detailed_description": {
                    "username": ["Este campo es requerido."] if not username else [],
                    "verification_code": ["Este campo es requerido."] if not verification_code else []
                }
            }
    except Exception as e:
        logger.exception(f"{g.request_id} - error in verification endpoint")
        g.response_code = "0400"
        return {
            "detailed_description": {"error": ["Datos inválidos"]}
        }

    return UsersService.verify_otp_code(username=username, verification_code=verification_code, request_id=g.request_id)

@bp.post("/reset-password")
@ServerUtils.configure_request(description_code_map=UsersConfig.reset_password_code_map, method="POST", endpoint="reset-password")
def reset_password():
    logger.info(f"{g.request_id} - starting reset_password")

    try:
        schema = UsersModel.reset_password()
        model = schema.load(request.json)
    except ValidationError as e:
        logger.error(f"{g.request_id} - validation error: {e.messages}")
        g.response_code = "0400"
        return {"detailed_description": e.messages}
    except Exception as e:
        logger.exception(f"{g.request_id} - error parsing request data")
        g.response_code = "0400"
        return {"detailed_description": {"error": ["Datos inválidos"]}}

    return UsersService.reset_password_with_token(model=model, request_id=g.request_id)

@bp.post("/resend-otp")
@ServerUtils.configure_request(description_code_map=UsersConfig.resend_otp_code_map, method="POST", endpoint="resend-otp")
def resend_otp():
    try:
        logger.info(f"{g.request_id} - starting resend_otp")

        data = request.json
        model = UsersModel.resend_otp().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    return UsersService.resend_otp(model=model, request_id=g.request_id)

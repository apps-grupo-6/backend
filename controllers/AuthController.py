from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from models import AuthModel, UsersModel
from configs import AuthConfig
from services import AuthService, UsersService
from utils import AuthUtils, ServerUtils

bp = Blueprint('auth', __name__)

@bp.post("/")
@ServerUtils.configure_request(description_code_map=AuthConfig.login_code_map, method="POST")
def login():
    try:
        logger.info(f"{g.request_id} - starting login")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = AuthModel.login().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return AuthService.login(model=model, request_id=g.request_id)

@bp.post("/otp")
@AuthUtils.validate_session
@ServerUtils.configure_request(description_code_map=AuthConfig.login_otp_code_map, method="POST", endpoint="otp")
def login_otp():
    try:
        logger.info(f"{g.request_id} - starting login_otp")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = AuthModel.login_otp().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return AuthService.login_otp(model=model, user_id=g.user_id, request_id=g.request_id)

@bp.post("/refresh")
@ServerUtils.configure_request(description_code_map=AuthConfig.refresh_token_code_map, method="POST", endpoint="refresh")
def refresh_token():
    try:
        logger.info(f"{g.request_id} - starting refresh_token")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = AuthModel.refresh_token().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return AuthService.refresh_token(model=model, request_id=g.request_id)

@bp.post("/verify")
@ServerUtils.configure_request(description_code_map=AuthConfig.verify_otp_code_map, method="POST", endpoint="verify")
def verify_otp():
    try:
        logger.info(f"{g.request_id} - starting verify_otp")

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

@bp.post("/resend-otp")
@ServerUtils.configure_request(description_code_map=AuthConfig.resend_otp_code_map, method="POST", endpoint="resend-otp")
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

@bp.post("/reset-password")
@ServerUtils.configure_request(description_code_map=AuthConfig.reset_password_code_map, method="POST", endpoint="reset-password")
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

from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from models import AuthModel
from configs import AuthConfig
from services import AuthService
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
    return AuthService.login_otp(model=model, request_id=g.request_id)

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

@bp.post("/recover")
@ServerUtils.configure_request(description_code_map=AuthConfig.recover_account_code_map, method="POST", endpoint="recover")
def recover_account():
    try:
        logger.info(f"{g.request_id} - starting recover_account")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = AuthModel.recover_account().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return AuthService.recover_account(model=model, request_id=g.request_id)

@bp.post("/recoverOtp")
@ServerUtils.configure_request(description_code_map=AuthConfig.recover_account_otp_code_map, method="POST", endpoint="recoverOtp")
def recover_account_otp():
    try:
        logger.info(f"{g.request_id} - starting recover_account_otp")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = AuthModel.recover_account_otp().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return AuthService.recover_account_otp(model=model, request_id=g.request_id)

@bp.post("/confirmAccount")
@ServerUtils.configure_request(description_code_map=AuthConfig.confirm_account_code_map, method="POST", endpoint="confirmAccount")
def confirm_account():
    try:
        logger.info(f"{g.request_id} - starting confirm_account")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = AuthModel.confirm_account().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return AuthService.confirm_account(model=model, request_id=g.request_id)

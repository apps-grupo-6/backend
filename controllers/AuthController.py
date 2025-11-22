from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from models import AuthModel
from services import AuthService
from utils import AuthUtils

bp = Blueprint('auth', __name__)

@bp.post("/")
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

@bp.post("/refresh")
@AuthUtils.validate_session
def refresh_token():
    logger.info(f"{g.request_id} - starting refresh_token")
    return AuthService.refresh_token(user_id=g.user_id, request_id=g.request_id)

@bp.post("/recover")
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

@bp.post("/confirm-account")
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

@bp.post("/logout")
@AuthUtils.validate_session
def logout():
    logger.info(f"{g.request_id} - starting logout")
    return AuthService.logout(user_id=g.user_id, request_id=g.request_id)
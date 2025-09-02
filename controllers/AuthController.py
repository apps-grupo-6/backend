from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from models import AuthModel
from configs import AuthConfig
from services import AuthService
from utils.AuthUtils import jwt_token_required

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
        return {"code": "0400",
                "description": AuthConfig.login_code_map["0400"],
                "detailed_description": e.messages
        }, 400

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return AuthService.login(model=model, request_id=g.request_id)

@bp.post("/otp")
@jwt_token_required
def login_otp():
    try:
        logger.info(f"{g.request_id} - starting login_otp")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = AuthModel.login_otp().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {"code": "0400",
                "description": AuthConfig.login_otp_code_map["0400"],
                "detailed_description": e.messages
        }, 400

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return AuthService.login_otp(model=model, request_id=g.request_id)
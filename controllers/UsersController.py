from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from services import UsersService
from models import UsersModel
from configs import UsersConfig

bp = Blueprint('users', __name__)

@bp.post("/")
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
            "code": "0400",
            "description": UsersConfig.register_account_code_map["0400"],
            "detailed_description": e.messages
        }, 400

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return UsersService.register_account(model=model, request_id=g.request_id)
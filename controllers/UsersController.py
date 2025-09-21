from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from services import UsersService
from models import UsersModel
from configs import UsersConfig
from utils import ServerUtils

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
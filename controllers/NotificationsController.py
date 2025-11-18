from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger
from utils import AuthUtils, ServerUtils

from configs import NotificationsConfig
from models import NotificationsModel
from services import NotificationsService
bp = Blueprint('notifications', __name__)

@bp.post("/setUserToken")
@ServerUtils.configure_request(description_code_map=NotificationsConfig.set_user_token_code_map, method="POST", endpoint="setUserToken")
@AuthUtils.validate_session
def set_user_token():
    try:
        logger.info(f"{g.request_id} - starting set_user_token")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = NotificationsModel.set_user_token().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return NotificationsService.set_user_token(model=model, user_id=g.user_id, request_id=g.request_id)
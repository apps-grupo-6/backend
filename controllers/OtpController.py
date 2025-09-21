from flask import Blueprint, g, request
from marshmallow import ValidationError

from configs.ServerConfig import logger

from services import OtpServices
from configs import OtpConfig
from utils import AuthUtils, ServerUtils
from models import OtpModel

bp = Blueprint('otp', __name__)

@bp.post("/")
@ServerUtils.configure_request(description_code_map=OtpConfig.create_otp_code_map, method="POST")
@AuthUtils.validate_session
def create_otp():
    try:
        logger.info(f"{g.request_id} - starting create_otp")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = OtpModel.create_otp().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return OtpServices.create_otp(model=model, user_id=g.user_id, request_id=g.request_id)
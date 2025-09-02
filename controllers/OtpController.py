from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from services import OtpServices
from models import OtpModel
from configs import OtpConfig

bp = Blueprint('otp', __name__)

@bp.post("/")
def create_otp():
    try:
        logger.info(f"{g.request_id} - starting create_otp")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = OtpModel.create_otp().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {"code": "0400",
                "description": OtpConfig.create_otp_code_map["0400"],
                "detailed_description": e.messages
        }, 400

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return OtpServices.create_otp(model=model, request_id=g.request_id)
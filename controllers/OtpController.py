from flask import Blueprint, g, request
from marshmallow import ValidationError

from configs.ServerConfig import logger

from services import OtpServices
from utils import AuthUtils
from models import OtpModel

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
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return OtpServices.create_otp(model=model, request_id=g.request_id)

@bp.post("/resend")
def resend_otp():
    try:
        logger.info(f"{g.request_id} - starting resend_otp")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = OtpModel.resend_otp().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return OtpServices.resend_otp(model=model, request_id=g.request_id)

@bp.post("/check")
def check_otp():
    try:
        logger.info(f"{g.request_id} - starting check_otp")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = OtpModel.check_otp().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return OtpServices.check_otp(model=model, request_id=g.request_id)

@bp.delete("/<int:id>")
@AuthUtils.validate_session
def delete_otp(id):
    logger.info(f"{g.request_id} - starting delete_otp")
    return OtpServices.delete_otp(otp_token_id=id, request_id=g.request_id)
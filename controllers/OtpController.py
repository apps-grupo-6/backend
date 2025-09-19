from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from services import OtpServices
from configs import OtpConfig
from utils import AuthUtils, ServerUtils

bp = Blueprint('otp', __name__)

@bp.post("/")
@AuthUtils.jwt_token_required
@ServerUtils.configure_request(description_code_map=OtpConfig.create_otp_code_map, method="POST")
def create_otp():
    logger.info(f"{g.request_id} - starting create_otp")
    return OtpServices.create_otp(user_id=g.user_id, request_id=g.request_id)
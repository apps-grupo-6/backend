from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from services import LocationsService
from models import LocationsModel
from configs import LocationsConfig
from utils import AuthUtils, ServerUtils

bp = Blueprint('locations', __name__)

@bp.post("/")
@AuthUtils.jwt_token_required
@ServerUtils.configure_request(description_code_map=LocationsConfig.create_location_code_map)
def create_location():
    try:
        logger.info(f"{g.request_id} - starting create_location")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = LocationsModel.create_location().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return LocationsService.create_location(model=model, request_id=g.request_id)
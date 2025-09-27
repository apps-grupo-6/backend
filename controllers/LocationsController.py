from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from services import LocationsService
from models import LocationsModel
from configs import LocationsConfig
from utils import AuthUtils, ServerUtils

bp = Blueprint('locations', __name__)

@bp.post("/")
@ServerUtils.configure_request(description_code_map=LocationsConfig.create_location_code_map, method="POST")
@AuthUtils.validate_session
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
    return LocationsService.create_location(model=model, user_id=g.user_id, request_id=g.request_id)

@bp.get("/")
@ServerUtils.configure_request(description_code_map=LocationsConfig.get_all_locations_code_map, method="GET")
#@AuthUtils.validate_session
def get_all_locations():
    logger.info(f"{g.request_id} - starting get_all_locations")
    return LocationsService.get_all_locations(request_id=g.request_id)
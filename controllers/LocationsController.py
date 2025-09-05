from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger

from services import LocationsService
from models import LocationsModel
from configs import LocationsConfig

bp = Blueprint('locations', __name__)

@bp.post("/")
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
            "code": "0400",
            "description": LocationsConfig.create_location_code_map["0400"],
            "detailed_description": e.messages
        }, 400

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return LocationsService.create_location(model=model, request_id=g.request_id)
from configs.ServerConfig import logger
from flask import g

from managers import LocationsManager
from configs import LocationsConfig

def create_location(model, request_id):
    owner_id = model['owner_id']
    country_code = model['country_code']
    city = model['city']
    address = model['address']

    logger.info(f"{request_id} - creating new location...")
    created = LocationsManager.create_location(owner_id=owner_id,
                                               country_code=country_code,
                                               city=city,
                                               address=address,
                                               request_id=request_id)

    if not created["ok"]:
        logger.critical(f"{request_id} - there was an error while creating")
        g.response_code = "0500"
        return {"code": "0500", "description": LocationsConfig.create_location_code_map["0500"]}, 500

    logger.info(f"{request_id} - location created successfully")
    g.response_code = "0200"
    return {
        "code": "0200",
        "description": LocationsConfig.create_location_code_map["0200"]
    }, 200

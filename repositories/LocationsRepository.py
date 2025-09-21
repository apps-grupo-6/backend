from managers import LocationsManager
from configs.ServerConfig import logger
from utils import ServerUtils

@ServerUtils.set_final_response
def check_if_location_exists(location_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if location_id '{location_id}' exists...")
    location_exists = LocationsManager.does_location_exist(location_id=location_id, request_id=request_id)

    if not location_exists["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if not location_exists["data"]:
        logger.error(f"{request_id} - invalid location_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - location exists")
    return {"flag": 1, "data": location_exists['data']}
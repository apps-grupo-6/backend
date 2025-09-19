from configs.ServerConfig import logger
from flask import g

from managers import LocationsManager, UsersManager
from repositories import UserRepository

def create_location(model, request_id):
    owner_id = model['owner_id']
    country_code = model['country_code']
    city = model['city']
    address = model['address']

    exists_user = UserRepository.check_if_user_exists(user_id=owner_id,
                                                      request_id=request_id,
                                                      errors_code_map={
                                                          "database_error_code": "0500",
                                                          "invalid_data_error_code": "0410"
                                                      })

    if exists_user["error"]:
        return {}

    logger.info(f"{request_id} - creating new location...")
    created = LocationsManager.create_location(owner_id=owner_id,
                                               country_code=country_code,
                                               city=city,
                                               address=address,
                                               request_id=request_id)

    if not created["ok"]:
        logger.critical(f"{request_id} - there was an error while creating")
        g.response_code = "0501"
        return {}

    logger.info(f"{request_id} - location created successfully")
    g.response_code = "0200"
    return {}

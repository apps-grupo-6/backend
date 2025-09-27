from configs.ServerConfig import logger
from flask import g

from managers import LocationsManager
from repositories import UsersRepository, LocationsRepository


def create_location(model, user_id, request_id):
    country_code = model['country_code']
    city = model['city']
    address = model['address']

    exists_user = UsersRepository.check_if_user_exists(user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map={
                                                           "database_error_code": "0500",
                                                           "invalid_data_error_code": "0410"
                                                       })

    if exists_user["error"]:
        return {}

    logger.info(f"{request_id} - creating new location...")
    created = LocationsManager.create_location(owner_id=user_id,
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

def get_all_locations(request_id):
    all_locations = LocationsRepository.get_all_locations(request_id=request_id,
                                                          errors_code_map={"database_error_code": "0500"})

    if all_locations["error"]:
        return {}

    g.respose_code = "0200"
    return {
        "data": all_locations["data"]
    }
